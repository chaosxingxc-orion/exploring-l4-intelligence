# Current Survey Status

- Gate: **Stage-1B v4 P0 repair frozen / narrow Stage-1C transition rereview pending**. The fixed
  scientific release is commit `f11a2b1fd0b6d81b08caefc5d576fe13ed579883`; Stage-1C has not started.
- Release identity: the v4 manifest binds 60 artifacts (52 Git, eight external). Commit-bound replay
  verifies 60/60 with zero missing, byte or SHA-256 mismatches.
- Evidence depth: the 81-work coverage ledger contains 70 `FULLTEXT_ROUTED` and 11
  `ABSTRACT_ROUTED` rows. All 70 full-text rows now have a successful full-text ledger record, local
  bytes and matching SHA-256. The seven v3 false-full-text defects are closed.
- Known priors: nine already-known works were reconciled to existing canonical work IDs. All nine use
  `REUSE_CANONICAL_WORK_ID`; no duplicate claim work or seed was created.
- Comparable surface: the v2 supplement has 39 rows—25 direct, 13 instruments and one boundary. The
  25 direct methods classify as nine external orchestration, nine state/event gated and seven
  evaluator/verifier gated; zero are coded as reward-guided selection.
- Eligible inputs remain unranked: budget/stop/repair, evaluator reliability and
  interactive/full-duplex are `ELIGIBLE_NON_H5`. Evidence-state and tool/agent arbitration remain
  ineligible while H5 is withheld.
- Asset facts are layered, not represented by one misleading whole-disk lock. The 31-entry frozen
  baseline is fully present. Stage-1C candidate assets and auxiliary assets are inventoried separately.
  Public VoiceAgentBench, Full-Duplex-Bench v3, Audio2Tool, Omni-DeepSearch and IHBench data are local
  and identity-pinned outside Git; related public repositories are commit-pinned where available.
- Known unavailable or unresolved assets remain explicit: exact tau-Voice data, LALM recordings,
  EchoChain code/data and the generated From Text to Voice corpus. Nearby datasets are not substituted.
- Data policy: dataset/checkpoint/output bytes stay under `SPEECHRL_DATA_DIR` and are never committed.
  Git retains only source URLs, immutable revisions/hashes, acquisition scripts and inventory receipts.
- Execution boundary: this repair issued no broad discovery, model/API call, metric run, reproduction,
  prototype, ranking, problem selection or novelty verdict.
- Next action: one independent rereview of commit `f11a2b1fd0b6d81b08caefc5d576fe13ed579883`
  against P0-R1 through P0-R4. A positive verdict may authorize Stage-1C common-rubric comparison only;
  model/reproduction execution remains separately withheld.
