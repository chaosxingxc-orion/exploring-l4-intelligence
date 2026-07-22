# Stage-1B Systematic Mapping Execution Plan

**Goal:** Execute the frozen system-first mapping, establish a canonical method-path evidence map, and
produce bounded Stage-1C inputs without making a novelty verdict or running any research model,
dataset experiment, smoke test, headroom test, or prototype.

**Authority:** Independent search-design `SIGN` for commit `c01fba7` followed by the owner's
2026-07-21 direction to begin Stage-1B. H5 is explicitly non-load-bearing until blind coder B and
third-party adjudication finish.

**Primary outputs:** REC-1 query receipts and raw hashes; REC-0 canonical screening ledger; REC-2
method-path records; citation-closure/saturation report; occupancy and unresolved tables; direct-prior
proximity and reproduction-readiness evidence; Stage-1C eligible evidence inputs.

## Workstream map

| WS | Question | Actions | Exit evidence | Stage boundary |
|---|---|---|---|---|
| 0 Authority and exposure | Can execution be replayed without overstating authority? | Bind commit, protocol/query hashes, actor, platform, exposure, and H5 hold | execution metadata + current status | No research-model or dataset touch |
| 1 Systematic discovery | What does the frozen search surface retrieve? | Run 65 arXiv rows with pagination/overflow splitting; scan 50 T1 routes; append the 2026-07-16→execution-date delta | REC-1/REC-7, raw hashes, retry/failure log | No query rewriting from observed results |
| 2 BFS and identity | What unique works survive title/abstract screening? | Merge aliases/versions without losing hit lineage; create one REC-0 per canonical work; dual screen conflicts | canonical-work map, flow counts, exclusion/unresolved ledger | Metadata cannot support mechanism claims |
| 3 Triggered DFS | Which works require full-text mechanism evidence? | Apply T-a/T-b/T-c/T-d; prioritize direct/core/claim-bearing and 2025+ work; fetch PDF+e-print; traverse method/comparison citations | D2 queue, full-text ledger, carry-forward ledger | FETCH is registered immediately |
| 4 Method-path coding | Which system cells and boundaries are occupied or unresolved? | Split mixed papers into paths; code 13 system axes, signals/LIVE edges, seven strict bits, information boundary, supply/verifier/budget reporting, quality and locators | REC-2, threat dual coding, occupancy/unresolved tables | No innovation-difference verdict |
| 5 H5 calibration | Are the seven speech/omni fields reliable enough to carry claims? | Blind 3×7 coder-B pass, agreement, third-party adjudication; recode only affected H5 rows if needed | calibrated H5 contract and disagreement report | H5 stays out of headlines until closed |
| 6 Citation closure | Is the inspected graph saturated under the preregistered rule? | Resolve identifiers; backward e-print + date-stamped forward snapshots; two consecutive zero-new-INCLUDED rounds | E1/E2/E3 report with total/resolved/ambiguous/unresolved | Resolved-subgraph dryness is not full closure |
| 7 Mapping synthesis | What facts can Stage-1C safely use? | Generate cellwise occupancy, negative priors/falsifiers, direct-prior proximity, limitations and improvement-space evidence | bounded Stage-1C input bundles | No final cards, ranking, selection, or reproduction freeze |
| 8 Release and handoff | Can a second party reproduce the mapping? | Re-run contracts, dual-platform checks and manifest binding; independent review | release-scoped reports and handoff | Stage-1C starts only after mapping close |

## Execution order and checkpoints

- [x] Record the scoped Stage-1B authorization and H5 hold in HOT/CURRENT.
- [x] Add a tested arXiv executor that preserves raw Atom bytes, hashes, REC-1 rows, pagination,
  deterministic overflow splitting, throttling, failures, and checkpoint resume.
- [x] Run the first frozen query and confirm the first REC-1/raw receipt pair.
- [x] Execute all 65 frozen arXiv rows in order; retry only through the bounded policy and retain failed
  requests as evidence.
- [x] Add a tested offline BFS snapshot builder that verifies every raw Atom hash and logged-ID list,
  deduplicates canonical arXiv IDs, and preserves all query-page lineage without making REC-0 decisions.
- [ ] Generate the execution-date delta batch without mutating the frozen prefix.
- [ ] Reverify and scan all 50 T1 routes into REC-7.
- [ ] Build the BFS hit union, canonicalize identities, and create REC-0 decisions with a second screen.
  The offline D0 union is built and hash-bound (20,727 IDs); identity resolution and dual-screen REC-0
  decisions remain open.
- [x] Enforce the paper-reading gate for the opening queue: D1 abstract analysis and a reasoned
  `SELECT_FULLTEXT|DEFER|EXCLUDE` decision precede acquisition; only `SELECT_FULLTEXT` papers may be
  downloaded and only local, hash-bound renditions may be read at D2.
- [x] Promote the opening P0 direct/core/claim-bearing works to D2; start with Omni-Decision, AOP-Agent,
  AudioToolAgent, Native Active Perception, Thinking While Listening, MM-ReAct, Agent-Omni and
  EChO-Agent. The opening D2 notes now cover 22 local full texts, including all 15 newly selected P0
  papers; all 10 P1 and 2 P2 records are also locally read in a separate method/measurement note.
  Citation-triggered promotions remain part of the continuing queue.
- [ ] Map the system, mechanism, measurement, safety, and boundary strata separately.
- [ ] Finish H5 blind calibration before using any H5 field in a headline or Stage-1C input.
- [ ] Run citation closure to E1/E2/E3 and report all unresolved/removal counts.
- [ ] Generate mapping outputs and request independent Stage-1B close review.

## Evidence questions used during coding

1. **RQ-SYS:** What state exists, who owns each decision right, which signal drives which LIVE edge,
   and what can repair, continue, stop, or synthesize?
2. **RQ-CTRL:** Do matched controls, ablations, alternative explanations, or negative results isolate
   controller value rather than candidate-supply, tool, or evaluator value?
3. **RQ-OMNI:** Which non-text observation/action path causally changes a later decision, at what
   temporal and evidence granularity?
4. **RQ-SAFE:** What prevents judge drift, reward hacking, unbounded loops, unsafe tool actions, or
   failure to abstain/stop?
5. **RQ-MEASURE-MAP:** Which supply conditions, candidate pools, oracle/upper-bound reports, equal-K
   baselines, budgets, verifier evidence, and missing attribution items are actually reported?

## Acceptance criteria

- Every discovery access has a stable class, timestamp, raw response or reconstructible ID set, and
  hash; reviewer-known items retain `query_recall_credit=false`.
- Every hit has one canonical REC-0 disposition; every INCLUDED REC-0 has exactly one REC-2; D2 rows
  have full-text locators recorded during coding.
- Every table states path/work denominators, task/modality and selection-object strata, and
  missing/unobtainable/conflict counts.
- Negative and conflicting evidence remains visible. `UNKNOWN` is not converted to a favorable false.
- H5 is absent from load-bearing derivations until independent calibration closes.
- The final Stage-1B package contains no project-generated WER/EM/headroom/effectiveness result and no
  novelty verdict.

## Stop and reopen rules

Stop mapping only at E1 ∧ E2 ∧ E3. Reopen after a new counterexample, identity mismatch, query-byte or
protocol change, unresolved load-bearing conflict, or evidence that invalidates a current path
classification. A reopen appends a dated batch; it never rewrites prior receipts or silently changes
the frozen query prefix.
