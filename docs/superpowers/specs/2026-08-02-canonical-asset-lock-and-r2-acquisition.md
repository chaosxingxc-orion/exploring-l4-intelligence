# Canonical asset lock and R2 acquisition

## Decision

`docs/datasets.lock.json` becomes the only current source for dataset, model and reference-asset
identity, lifecycle, acquisition state and local verification. The former candidate and gap manifests
are historical inputs only and are retired after every live reference has been moved to the lock.

This transaction authorizes data acquisition only. It does not authorize model execution, experiments,
repository creation for a study, or a Stage-2 result claim.

## Required semantics

Every asset record must distinguish:

1. `lifecycle`: why the asset is retained (`FROZEN_BASELINE`, `LOCAL_CANDIDATE`, `STAGE2_CORE`,
   `DIAGNOSTIC`, `DEFERRED`, `RESTRICTED`, `SOURCE_UNSTABLE`, or `UNAVAILABLE`);
2. `status`: what is actually on this machine (`COMPLETE`, `PARTIAL`, `MISSING`, or `BLOCKED`);
3. `source`: the authoritative upstream identity and access method;
4. `revision`: an immutable upstream revision or an explicit explanation of why no pin exists;
5. `verification`: what was checked locally and when;
6. `profiles`: named fetch groups, so a default command never silently downloads the entire catalog.

The frozen June/July baseline remains a fetch profile; it is no longer confused with the complete
catalog. A record with `status=COMPLETE` is not automatically paper-exact reproducibility: protocol,
implementation and numerical-reproduction limits remain explicit in the record.

## R2 acquisition scope

- Core: Earnings21 original, Earnings22 original, and ConEC.
- Diagnostics: PRISM public synthetic set, a locally derived Rare5k protocol, and BuzzWord.
- Secondary public carriers: SLUE-SQA-5 and ContextASR-Bench.
- Annotation-only: TED-EL; TED-LIUM3 stays `SOURCE_UNSTABLE` until a trusted archive matches the
  historical SHA-256.
- Small optional public material may be fetched after the core: ATCO2 1-hour test set, Eka-Medical,
  and LibriSQA metadata.
- Restricted, unstable, private, or non-load-bearing corpora are cataloged but never bypassed or
  downloaded from an untrusted mirror.

## Gates

- `lock validate`: schema, unique identities, valid lifecycle/status values, source pins and profiles.
- `fetch`: reads only the lock and writes a local acquisition receipt; named profile or names required
  outside the frozen baseline.
- `inventory`: reads only the lock; no hard-coded dataset roster.
- R2 D0: exact commits, complete LFS materialization, no partial markers, and per-source receipts.
- R2 D1-D4 remain protocol/loader checks and are not implied merely by successful download.

## Supersession and failure policy

The lock is superseded in place. Release-scoped download/check receipts are immutable once referenced.
If an upstream is gated, missing, or unstable, record `BLOCKED`/`MISSING` with the reason; do not replace
it with an unofficial copy. If a download is interrupted, retain resumable bytes and mark `PARTIAL`.

