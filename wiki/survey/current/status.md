# Current Survey Status

- Gate: **Stage-1B release frozen / transition review pending**. Release commit is
  `8101320a1a25c3628a5d5c196b2efceb83abe829`; formal Stage-1C start requires an independent signature.
- Exposure: 65 frozen arXiv rows and 65/65 bounded delta rows executed; research model/smoke = 0;
  dataset metric/reproduction/prototype = 0. Broad D0 scanning remains closed.
- Frozen D0: 20,727/20,727 abstract identities, 319 D2 full texts, 226 retained works = 12 core +
  43 instrument + 45 transfer + 126 negative; 93 drop, 0 disposition unresolved. This is D0
  exhaustion, not literature-universe closure.
- Delta: 193 unique candidates for 2026-07-16..2026-07-21; 12 selected once at REC-0 and acquired as
  PDF+e-print+D2; 181 excluded only from this release's load-bearing map; duplicate seeds = 0.
- T1: 50/50 route dispositions = 28 executed + 3 not held + 19 `WAIVED_UNAVAILABLE`. Executed routes
  contain 71,254 titles and 3,310 wordlist matches; 677 reconcile to known works and 2,633 remain
  title-only. Waived/title-only items do not support zero-hit or `NO_DIRECT_MATCH` claims.
- Citation closure: all 12 frozen registry core works have local e-print backward extraction;
  266 unique arXiv-ID edges, 232 outside D0/delta/registry. DOI/title-only edges remain unresolved.
  Forward index access returned HTTP 429, so 12/12 forward routes are explicitly waived and no
  full-citation-closure claim is made.
- Mapping denominators: 226 unique portfolio works; strict occupancy = 8 works / 11 paths (9
  load-bearing, 2 boundary); delta supplement = 12 D2 works outside the frozen 226 denominator.
  The same work is not duplicated across role facets.
- Strict sensitivity: 11/11 paths are API-only; 7 text-native, 4 vision-native, 0 speech-native;
  the speech count is unmeasured strict coding, not evidence that the literature cell is empty.
- Required products: coverage/kill, occupancy, task/modality/access sensitivity, instrument/negative,
  saturation/flow, proximity/readiness and limitations are in `tables/stage1b-mapping-release.md`.
- Eligible inputs: `tables/stage1c-eligible-inputs.md` is unranked. Budget/stop/repair, evaluator
  reliability and interactive/full-duplex are `ELIGIBLE_NON_H5`; evidence-state and tool/agent
  arbitration are `INELIGIBLE_FOR_STAGE_1C_SELECTION` pending H5.
- H5: coder-A 21/21 anchors and blind packet exist; independent coder-B, agreement and third-party
  adjudication are pending. H5 contributes zero load-bearing occupancy/headline/selection rows.
- Reproduction boundary: existing ASR/omni feasibility documents are `PROVISIONAL_INPUT /
  NOT_STAGE_FROZEN`. Stage-1B does not rank problems or freeze a reproduction list; Stage-2A owns
  execution after Stage-1C selection and a separate authority gate.
- Integrity correction: eight historical invalid `--help` request rows remain append-only in the
  full-text ledger and are excluded from paper/rendition denominators. The CLI now rejects invalid IDs
  before network access; no source rows were deleted.
- Release verification: 35 manifest artifacts = 29 Git + 6 external; commit/external byte and SHA-256
  replay reports zero mismatches; the release commit adds no PDF/e-print.
- Next action: request one independent Stage-1C transition review against commit `8101320`; no model,
  smoke, ranking, selection or reproduction action is next.
