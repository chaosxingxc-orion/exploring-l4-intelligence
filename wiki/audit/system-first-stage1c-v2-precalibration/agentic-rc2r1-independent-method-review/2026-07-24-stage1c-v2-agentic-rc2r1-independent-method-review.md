---
title: "Stage-1C v2 Agentic RC2R1 independent method review"
date: "2026-07-24"
artifact_type: "INDEPENDENT_AI_DOCTORAL_SUPERVISOR_ADVISORY_REVIEW"
campaign: "system-first-stage1c-v2-precalibration"
round: "agentic-rc2r1-independent-method-review"
reviewed_commit: "8d0a7c62a99cc93ff394881f20ad793e308f3342"
review_manifest_path: "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r1/review-package-manifest-rc2r1.json"
review_manifest_git_blob: "50bfe3ba01f7cc908403d8a5979651fc868fb238"
review_manifest_sha256: "436da1dc1d103fb8611fc75fe86a68a75ffbf6bf16908c7c3ea5441d051d73c2"
verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
human_signature_claimed: false
owner_authority_effect: false
coder_role_claimed: false
repository_modified_by_reviewer: false
---

# Independent method review

## Independence and evidence boundary

This is an AI doctoral-supervisor advisory review, not a human signature, owner ruling, coder output
or adjudication. The reviewer used a fresh no-fork context and inspected only commit
`8d0a7c62a99cc93ff394881f20ad793e308f3342` through Git object bytes. It made no repository edits and
performed no literature discovery, research-model call, benchmark, reproduction or prototype.

The exact manifest contains 26 unique artifacts. The reviewer independently recomputed their bytes
and SHA-256 values from Git blobs: 26/26 matched. Predecessor commit
`74cf8e4b565a9e53ff40f9dbc34961ede853dd57` is an ancestor, and all 22 artifacts in the predecessor
RC2 review manifest retain identical Git blobs: 22/22 unchanged.

## Findings that pass

### Exact-size and completed-response checks

The v3 engine rejects 55/56 response sets, the wrong canonical-ID set, duplicate response IDs,
`NOT_CODED`, wrong coder/transaction/source/packet bindings and non-submitted responses. Both sets
must contain 56 unique records; coder, transaction and process identities must be distinct.

### Per-path agreement gates

Thirteen paper-level critical fields are independently gated. Nine object types receive independent
segmentation gates and 77 critical object-field paths receive separate exact-agreement gates: 99
load-bearing gates in total. A zero denominator is `NOT_CALIBRATED`; any `FAIL` or `NOT_CALIBRATED`
prevents overall PASS. The former aggregate-field dilution defect is closed.

### Reference, transfer and reproduction structure

Under the exact v3 schema, BORROW_PROTOCOL requires source protocol, target speech/omni variables,
preserved decision structure, locators, rejection condition and rejection observable.
REPRODUCTION_CANDIDATE requires task, dataset revision/split, official repository and pinned
revision, entrypoint, access, terms, evaluator/ground truth, local state, locators, CLOSED status and
no blockers. REFERENCE cannot carry transfer or reproduction evidence.

### ACL receipts and predecessor immutability

Both ACL records have official record/PDF URLs, publication revision, verification timestamp and
independent receipt IDs. Receipt bytes and SHA-256 match the source manifest and rehashed local PDFs:

- `acl:2026.acl-long.1615`: 577349 bytes,
  `081805a63ca2ef8fa04b1378d6aa2cda86b904d3cf9ccd5f0d496593df86a6b1`;
- `acl:2026.findings-eacl.151`: 1270881 bytes,
  `da6a78305f6f62dcf38a88b4f2d3a9be93001c3d5591ee621dae6463cffc153c`.

This proves commit-bound receipt/local-byte identity, not a new content review or fresh redownload.

### Cross-platform and execution boundary

The deterministic checker and 17 tests passed on Windows and WSL2 Ubuntu-24.04. Branch-aware
coverage was 92–93% for agreement, 87% for the builder/validator and about 89% combined. The package
still records zero coder distribution, agreement, research-model call, benchmark metric, paper
reproduction, prototype, anchor promotion, novelty verdict, full mapping, Stage-2A or push.

## Blocking bounded defects

### P0-1: self-consistency does not prove frozen-package identity

`compute_agreement()` checks that runtime intake is internally self-consistent, but not that it is the
exact frozen RC2R1 intake. It does not validate exact artifact/calibration/source/distribution IDs
against commit-bound digests. Bundle and prompt fields only need to be 64-hex values repeated in both
slots. Schema binding compares only `$id`, not exact schema bytes or SHA-256.

Minimal reproduction: replace the intake IDs, all 56 canonical IDs and packet bindings, source IDs,
bundle hash and prompt hash with another internally consistent set, and mutate both response sets to
match. The engine still computes `paper_count=56`. This proves an arbitrary 56, not the frozen 56.

Required repair:

- freeze a base-intake digest and the exact calibration, source, distribution, response-schema,
  shared-bundle and prompt digests;
- validate runtime intake's static projection against those committed digests;
- reject a completely substituted but internally consistent 56-item universe.

### P0-2: same-ID lax schema and unbound rendition bypass evidence closure

Because the engine compares only schema `$id`, a permissive replacement schema with the same `$id`
can accept incomplete BORROW evidence. Locator validation only proves that evidence references a
locator declared inside the same response. It does not prove that `rendition_id` belongs to that
paper in the frozen source manifest; a fake or cross-paper rendition can support BORROW evidence.

Required repair:

- bind and validate exact response-schema bytes/hash, not only `$id`;
- build a frozen `paper_id → allowed rendition IDs/bytes/hash` map;
- reject fake and cross-paper rendition IDs before completed-response acceptance.

### P0-3: actual delivery receipts are opaque identifiers

The package proves the intended shared content hash. Runtime slots only require non-empty
distribution/submission receipt IDs and repeat expected hashes. No field proves the bundle/prompt
hash actually received by each coder; no receipt artifact digest is checked by agreement intake.

Required repair:

- record each coder's actual received bundle and prompt hashes, or bind a hashed receipt artifact;
- require both actual hashes to equal the frozen distribution manifest before accepting responses.

### P1: value exception is keyed by leaf name rather than exact path

The scanner is recursive, but the blind-packet exception accepts any `title` leaf. Adding a forbidden
expectation under `auxiliary_metadata.title` produces no finding. Source titles are legitimate, but
the exception must be restricted to the exact source-title JSON path.

Required repair: use exact JSON-pointer patterns such as `$.blind_packet.items[*].title` and add
negative tests for the same leaf name under other metadata paths.

## Verdict

`WITHHOLD_WITH_BOUNDED_DEFECTS`

RC2R1 closes prior dilution and structured-evidence defects, preserves RC2 and improves ACL
provenance. It remains unsafe for coder intake because agreement can run on a self-consistent but
non-frozen universe, incomplete evidence under a same-ID schema, fake/cross-paper renditions and
opaque delivery receipts. High coverage does not close these untested bypasses.

The repair is bounded to provenance-chain validation, exact schema/rendition binding, delivery
receipts, exact-path leakage exceptions and negative tests. No new literature, 320 mapping or
research execution is needed.

This verdict grants no repair, distribution, coder, agreement, mapping, research, portfolio,
Stage-2A, push or signature authority. Owner authorization remains required.
