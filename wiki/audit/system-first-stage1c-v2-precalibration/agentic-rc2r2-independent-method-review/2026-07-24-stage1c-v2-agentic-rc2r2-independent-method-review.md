---
title: "Stage-1C v2 Agentic RC2R2 independent method review"
date: "2026-07-24"
artifact_type: "INDEPENDENT_AI_DOCTORAL_SUPERVISOR_ADVISORY_REVIEW"
campaign: "system-first-stage1c-v2-precalibration"
round: "agentic-rc2r2-independent-method-review"
reviewed_commit: "9652d98eade798903be6c5d007591d2602a2f5c3"
review_manifest_path: "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r2/review-package-manifest-rc2r2.json"
review_manifest_git_blob: "b3d09f2652b8bd976047bac4fe4ea6ef48488464"
review_manifest_sha256: "628081eefc584e7a58625bb5cda4df58ec02ba2e75536956b9caa61e96086f17"
verdict: "WITHHOLD_WITH_BOUNDED_DEFECTS"
human_signature_claimed: false
owner_authority_effect: false
coder_role_claimed: false
repository_modified_by_reviewer: false
---

# Independent method review

## Independence and evidence boundary

This is a fresh, no-fork AI doctoral-supervisor advisory review. It is not a human signature,
owner ruling, coder output or adjudication. The reviewer inspected only commit
`9652d98eade798903be6c5d007591d2602a2f5c3` through Git object bytes and the exact RC2R2 review
manifest. It made no shared-repository edit and performed no literature discovery, research-model
call, benchmark, reproduction or prototype.

## Exact identity and predecessor checks

The review manifest contains 30 unique artifacts. The reviewer independently read each artifact with
`git show <commit>:<path>` and recomputed length and SHA-256: 30/30 matched. RC2R1 commit
`8d0a7c62a99cc93ff394881f20ad793e308f3342` is an ancestor. Its manifest retains Git blob
`50bfe3ba01f7cc908403d8a5979651fc868fb238`; all 26 RC2R1 artifacts match in both trees, and the
reused agreement-v3 dependency retains blob `1165549193e873a729c5377ecbbdf2bfc3d221f8`.

Independent recomputation also matched:

- compiled frozen contract: `e039074f5897c43fb6a26dc2bdb58bb41e52426c87c7631adec54dbe461e262f`;
- eight-artifact coder bundle: `b4bfb18030a08e010fb32c5ceea7853e1f6b1dbf83c1bcc1d9de078b6f69cb04`;
- coder prompt: `88fca5a601bc49b946e2c29fcac35ba212dec38af5625c312a964535201aaa8e`;
- static intake projection: `b5f918b12837647f76f366b1e57423ef2ff022ace6ed6990ae0864cff39a19b3`;
- canonical-ID sequence: `1e4bad7836d8312d2444f3847b10e6c928537ac7b60fe35df5c1a6cde81f1b0d`;
- paper-scoped rendition map: `38f8116d6a9d84275f5e75f6f3b22093e0be300ccf9765894f84263ec0e52908`.

## Findings that pass

### Frozen package, N=56 and source binding

The compiled literal matches the frozen-contract digest. Under SHA-256 collision resistance, a
caller cannot replace all artifacts with a second internally consistent 56-item universe without
changing agreement code. The runtime static projection binds the ordered 56 canonical IDs, 56
paper/packet/source bindings, calibration/source/distribution/schema IDs, bundle/prompt digests and
the planned A/B models. Cross-checking calibration, blind packet and source manifest produced zero
mismatches.

The source manifest contains 56 unique papers, 56 unique source items and 135 globally unique
rendition IDs. Exact schema hashing rejects a same-`$id` lax schema. Paper-scoped rendition checks
reject fake and cross-paper locators.

### Existing semantic and agreement gates

The v4 response schema differs from v3 only at the version identity fields, so the unchanged v3
REFERENCE/BORROW/REPRODUCE semantic validator remains active. Agreement retains 13 paper gates, nine
object-segmentation gates and 77 independent critical object-field gates: 99 load-bearing gates.
Zero denominators remain `NOT_CALIBRATED` and cannot produce overall PASS.

### Test, regeneration and authority evidence

In an isolated short-path checkout, Windows passed 17/17 RC2R2 tests and 62/62 RC2+RC2R1+RC2R2
regression tests. Branch-aware coverage reproduced at 89% for agreement, 88% for the builder and 88%
combined. WSL2 Ubuntu-24.04 with the required `~/.venvs/speechrl` environment passed 17/17. On both
platforms, `--write` left tracked bytes unchanged.

The exact package records distribution unauthorized, both coder slots unassigned, agreement intake
prepared-not-distributed, zero eligible anchors/reproductions/research executions and no mapping,
Stage-2A or push authority.

## Blocking bounded defects

### P0-1: the frozen 0.85 agreement threshold is runtime-overridable

`agreement-contract-v4.json` fixes `minimum_gate_value=0.85`, but `compute_agreement()` accepts any
caller-supplied `minimum` in `(0,1]`. Neither the frozen contract nor static intake binds that runtime
value. A 0.50 observed agreement is FAIL at 0.85 but PASS at 0.01, so a caller can weaken all
non-empty critical gates without changing a frozen artifact.

Required bounded repair:

- remove the public threshold override or require it to equal an engine/frozen constant of 0.85;
- bind the threshold into the frozen trust contract;
- add negative tests for `0.84`, `0.01` and other non-contract values.

### P0-2: delivery receipt copies expected hashes without observing received bytes

`build_delivery_receipt(package, ...)` receives no actual bundle, prompt or artifact byte streams. It
copies expected values out of the distribution manifest into `received_*`, self-hashes that assertion,
and the validator compares it back to the same manifest. The reviewer generated and validated the
whole delivery chain with zero received-byte inputs. The digest prevents later receipt mutation, but
does not prove what a coder actually received or detect a one-byte delivery error.

Required bounded repair:

- create the receipt at the coder-receive boundary from the actual eight artifact byte streams and
  actual prompt bytes;
- independently recompute per-artifact, prompt and combined bundle digests from those bytes;
- bind the receiver-produced receipt bytes/digest to slot, transaction and process;
- reject receipt creation without actual bytes and add a one-byte-corruption negative test.

### P1-3: string-built JSON paths admit structural aliases

The scanner concatenates unescaped path strings. A literal object key `"items[0]"` under
`blind_packet` produces the same string path as a real array element. Adding
`blind_packet["items[0]"]["title"]` with a forbidden named expectation returns no finding; after
consistent digest regeneration, the package validator also accepts it. Existing tests cover
`auxiliary_metadata.title` but not bracket/dot/slash key aliases.

Required bounded repair:

- represent paths as typed key/index segments or escaped RFC 6901 JSON Pointers;
- do not distinguish object keys and array indices through concatenated display strings;
- reject unexpected blind-packet top-level properties with a strict schema or equivalent guard;
- add negative tests for literal keys containing brackets, dots, slashes and pointer escapes.

## Portability notes

A deeply nested Windows temporary checkout can hit Git filename-length limits; the repository's
normal short path and the reviewer's short-path checkout pass. In the WSL venv, an installed package
named `scripts` can shadow repository namespace-style module invocation; direct test-script execution
passes. These are reproducibility notes, not the withholding basis. Future verification receipts
should retain exact cwd, command, interpreter, exit code and post-write diff exit code rather than
only a summarized result.

## Verdict

`WITHHOLD_WITH_BOUNDED_DEFECTS`

The compiled root, exact N=56 static projection, schema/rendition binding and predecessor
immutability repairs substantially close the RC2R1 defects. Coder intake nevertheless remains unsafe
because the agreement threshold is caller-controlled, delivery provenance is circular expected-value
self-attestation, and exact-path exceptions still have a structural alias. These repairs are bounded;
they require no new literature, research model, benchmark, reproduction or prototype.

This verdict grants no repair, distribution, coder, agreement, mapping, adjudication, research,
portfolio, Stage-2A, push or signature authority. The owner must decide whether to authorize a new
immutable successor repair.
