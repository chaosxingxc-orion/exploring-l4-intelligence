# Stage-1C v2 Agentic completion execution plan

Date: 2026-07-25

State: `R2_CONSOLIDATION_AUTHORIZED_IN_PROGRESS`

Scope: finish calibration, 320-work evidence mapping, experiment-family synthesis, K/S/M × control
analysis, local protocols, branch portfolio and the detailed Chinese research proposal. This plan
does not itself grant any gated authority.

## 1. Definition of done

Stage-1C is complete only when all of the following are simultaneously true:

1. a calibration release with two frozen raw N=56 outputs, pre-adjudication agreement, complete
   disagreement/adjudication provenance and independent method/release review is signed;
2. `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` is registered against an exact manifest;
3. the immutable 320-work union is audited exactly once per canonical ID, with 56 valid calibrated
   carry-forwards and 264 new primary records;
4. every in-scope empirical work has source-located experiment cells/observations, while exclusions
   and non-empirical works remain evidence nodes rather than fabricated cells;
5. dataset lineage/relation, experiment families and comparability rules pass machine and human
   review;
6. families are mapped horizontally onto Knowledge, Skill, Memory × system/control without replacing
   the experiment-family primary axis;
7. every locally feasible family has a `NOT_EXECUTED` protocol and every branch is either
   `READY_FOR_FUNNEL` after all five gates or `REFERENCE_ONLY` with reasons;
8. the Chinese research proposal and unranked branch portfolio pass independent review and receive
   `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO`;
9. CURRENT, manifests, audit registry and archive routing reproduce on Windows and WSL; and
10. research-model calls, benchmark metrics, paper reproduction, prototype execution and project
    novelty verdict remain zero.

Stage-2A is not part of this completion definition and still requires
`AUTHORIZE_STAGE2A_AGENTIC_REPRODUCTION_FUNNEL`.

## 2. Current evidence and remaining gates

Completed evidence:

- immutable Stage-1B v5 and signed capability/anchor overlays form the 320-work union;
- RC2R3 method contract was independently accepted;
- R1 Sol/Terra coding completed exact N=56, and both raw byte streams froze before agreement;
- R1 paper-level gates passed 5/13 and failed 8/13; all nine object types had zero common match keys;
- all 232 paper-field disagreements and unmatched objects are preserved; no adjudication was used to
  rewrite raw scores.

Open gates, in order:

| Gate | Exact authority/evidence | Current state |
|---|---|---|
| G1 | `AUTHORIZE_STAGE1C_V2_AGENTIC_CALIBRATION_R1_CODEBOOK_CONSOLIDATION` | authorized 2026-07-25 |
| G2 | independent ACCEPT of the consolidated R2 method package | not started |
| G3 | owner adjudication of R2 carrying disagreements | not started |
| G4 | independently reviewed calibration release | not started |
| G5 | `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` | required after G4 |
| G6 | owner adjudication of 320-work carrying disagreements | not started |
| G7 | independent portfolio/proposal review | not started |
| G8 | `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO` | required for completion |

No later gate may be inferred from an earlier token.

## 3. Legacy cleanup policy

“Cleanup” means removing active contradictions, not rewriting history.

- Refresh HOT/CURRENT/Per-Work statements that still describe R1 responses as pending.
- Preserve distribution manifests, prior RC packages, raw coder outputs and registered audit
  transactions at their historical status.
- Treat old 226-work mapping packages as historical design references. A new 320-work Agentic
  campaign must not silently activate the old generator.
- Keep specialized Duplex work only as the single exclusion boundary; do not spend research effort
  on its method path.
- Keep H5 pending as an explicit information boundary. It does not block non-H5 mapping, but no
  modality-specific or cross-modal conclusion may depend on it.
- Archive superseded unregistered work only after manifest, inbound-link and safe-move checks pass.

## 4. Phase A — one bounded calibration consolidation

This phase starts only after G1. R1 remains immutable and the successor receives new schema, package,
prompt and manifest IDs.

### 4.1 Object identity and agreement

The R1 failure showed that coder-authored `object_match_key` is not a valid agreement identity.
R2 must separate three concepts:

1. `source_anchor`: a compiler-generated identifier for rendition hash + page/block/table/row;
2. `segmentation_signature`: deterministic object-type + paper ID + source anchor + mechanically
   normalized identity tuple;
3. `content_identity`: the substantive run/dataset/claim fields whose agreement is measured only
   after segmentation alignment.

Coders select source anchors and enter semantic fields; they never invent match keys. The compiler
generates signatures and cross-object references. Exact matching remains mandatory; post-hoc fuzzy
matching is prohibited.

For object gates, the denominator is the union of aligned and unmatched objects. An unmatched object
counts as disagreement for segmentation and each applicable critical field; it must not turn the
field denominator into zero. `NOT_CALIBRATED` is reserved for a true zero-positive class where both
coders legitimately emit no object.

### 4.2 Object trigger and extraction completeness

- `EMPIRICAL_EXTRACTABLE` requires all material run cells, observations and dataset nodes supported
  by the frozen source, not a one-object-per-paper shortcut.
- Multiple metrics stay under one run; a material run-condition change creates a new cell.
- A paired comparison is mandatory when baseline/intervention and the comparability key close; an
  explicit typed absence reason is required otherwise.
- A source-backed dataset lineage or relation creates an edge; semantic similarity alone cannot.
- `BORROW_PROTOCOL` requires both translation and protocol-transfer objects.
- Source locators must support object identity and carrying fields, not merely the title or abstract.

### 4.3 Reference, borrowing and reproduction

R1 combined paper-source reproducibility with local repository state while forbidding blind coders
from seeing the repository. R2 must split them:

- blind `paper_reproduction_support`: task, dataset/revision/split, official repo/revision,
  entrypoint, access, terms, evaluator and source locators reported by authorized source bytes;
- reviewer-only `local_reproduction_readiness`: pinned checkout, local assets, loader, access,
  license/terms acceptance and blockers;
- `REPRODUCTION_CANDIDATE` requires complete paper support, but `REPRODUCTION_ANCHOR` additionally
  requires reviewer/local closure and later 100% review;
- `REFERENCE` transfers neither protocol nor results; `BORROW_PROTOCOL` preserves only an explicit
  decision structure with source→speech/omni translation and a rejection observation.

This preserves the distinction among reference, borrowing, candidate, local readiness and anchor.

### 4.4 Positive-support preflight

Before R2 distribution, a reviewer-only coverage checker must prove at least one source-supported
positive for every object class whose gate is required to pass. The coder-visible packet must not
contain expected labels or selection rationales.

The completed read-only R1 preflight establishes:

- `dataset_edges` has two source-supported positives in TRACE page 3 (`SUBSET_OF` and
  `REANNOTATED_FROM`), while both R1 coders emitted zero; this is an extraction-trigger failure;
- the current `reproduction_evidence` contract has zero support because it requires blind coders to
  report `local_asset_state`, forces `closure_status=CLOSED` and forbids blockers while repository
  access is explicitly withheld; this is an observability contradiction, not evidence of absence.

R2 therefore treats paper-visible reproduction candidacy as a typed record that may remain
`OPEN_WITH_BLOCKERS`. Only reviewer-side local readiness can promote it to a closed reproduction
anchor. After that semantic split, the positive-support checker must run again against the exact R2
schema and source packet. If the unchanged N=56 still cannot support a mandatory positive,
distribution stops. Adding neutral official source renditions or replacing a sentinel requires a
separately recorded bounded repair and fresh method review; the checker may never manufacture a
positive.

### 4.5 Paper decision tables

Compile mutually exclusive examples and counterexamples for:

- paper role and empirical disposition;
- `REFERENCE` / `BORROW_PROTOCOL` / `REPRODUCTION_CANDIDATE`;
- access regime and generic frozen core / trained controller / specialized model;
- direct/instrument/transfer/reference-boundary/specialized exclusion scope;
- loop components, K/S/M assets and the unique primary intervention axis.

Specialized Duplex and trained-controller exclusions remain unable to produce cells, CORE membership,
reproduction anchors or branch primaries.

## 5. Phase B — R2 calibration execution

After independent method ACCEPT:

1. create two new no-fork Sol/Terra contexts and separate no-`.git` workspaces;
2. deliver byte-identical coder-visible bundles with receiver-side byte receipts and the same prompt
   hash;
3. encode all 56 papers in each persistent context; no coder sees repository state, prior labels,
   another response or new network discovery;
4. validate exact IDs, schema, semantics, source anchors, compiler-derived identities and positive
   coverage;
5. freeze both raw outputs before computing any agreement;
6. compute every paper, segmentation and critical-field gate at fixed 0.85;
7. submit all carrying disagreements to the owner without altering raw scores;
8. freeze the adjudication log and independently review the release.

This is the only allowed recode. If any calibrated critical gate remains below 0.85, or any mandatory
class remains `NOT_CALIBRATED`, Stage-1C stops and returns to independent method review.

## 6. Phase C — exact mapping signature

After the calibration release passes review, build an exact commit-bound submission containing:

- immutable 320-work union identity/hash;
- calibrated R2 release and carry-forward rules;
- full-mapping response schemas and Agentic scope rules;
- review sampling algorithm/seed and 100% carrying-object review rules;
- no-execution, H5 and Duplex boundaries.

Only the exact `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING` opens full mapping.

## 7. Phase D — 320-work paper audit and experiment extraction

Create a new Agentic mapping campaign:

- 56 adjudicated calibration records carry forward without recoding their calibrated fields;
- 264 remaining works receive primary coding;
- final coverage is exactly 320 unique canonical IDs, with no unexplained exit;
- only in-scope empirical Agentic works produce experiment cells;
- non-empirical, trained-controller and specialized-system works remain evidence nodes;
- each cell binds paper × dataset revision/split × model/access × input × intervention × budget;
- observations contain metrics/results; multiple metrics never duplicate cells;
- cross-paper numeric synthesis requires the complete exact comparability key;
- all source claims use exact locators.

Blind review uses a frozen seed to select 64 of the non-calibration 264 records, stratified by
Stage-1B role, source domain and task metadata. CORE_MEMBER assignments, lineage claims,
reproduction anchors, family conclusions and branch cards receive 100% second review. Owner resolves
all carrying disagreements.

If Knowledge, Skill or Memory lacks a task-matched direct/reproduction anchor, pause only that axis
and request `AUTHORIZE_STAGE1B_AGENTIC_ANCHOR_DELTA`; never launch silent broad discovery inside
Stage-1C.

## 8. Phase E — experiment families and capability synthesis

Family construction precedes capability abstraction. The primary signature is:

`target failure/problem × evaluation object/outcome semantics × environment/access × interpretable baseline→intervention comparison`.

Membership remains typed:

- `CORE_MEMBER`: directly compatible;
- `VALIDATION_MEMBER`: independent dataset or shift validation;
- `TRANSFER_ANALOGUE`: visual/text protocol with source→target translation and rejection condition;
- `FALSIFIER`: challenges the capability, metric or strategy;
- `INSTRUMENT_SUPPORT`: evaluator/calibration/measurement support.

Only after family cards close, map them onto:

- capability assets: Knowledge, Skill, Memory;
- carrier: multimodal Agent system;
- control: training-free reward-guided, training-free non-reward, trained boundary, instrument-only;
- secondary mechanisms: observe/evidence, state, supply, evaluate, route/select, budget/stop,
  repair/rollback, tool/environment and interaction recovery.

Each cell has one primary intervention attribution. Combination gains remain system-bundle evidence
unless factorial/ablation evidence separates their causes.

## 9. Phase F — local protocols and branch portfolio

Every `LOCAL_READY` or closable `LOCAL_ADAPTABLE` family receives an unexecuted protocol binding:

- dataset/revision/split and loader/adapter;
- frozen-core model/access;
- evaluator/ground truth;
- baseline, intervention, budget/horizon and failure/harm axes;
- license/terms and blockers;
- falsifier and kill criterion;
- execution state `NOT_EXECUTED`.

A branch is `READY_FOR_FUNNEL` only if all five gates pass: local readiness, falsifiable residual,
task-matched nearest prior, observable outcome/evaluator, and strongest falsifier + kill criterion.
Each ready branch has four arm classes: one-call frozen baseline, nearest-prior reproduction,
candidate strategy, and oracle/upper bound or a typed non-definability reason. No branch quota or
ranking is imposed.

## 10. Phase G — Chinese research proposal and closeout

The final Chinese proposal must contain:

1. 320-work evidence census and exclusion accounting;
2. experiment-family map and stratified evidence conclusions;
3. K/S/M × carrier × control capability graph;
4. primary, validation, falsifier, transfer and instrument families;
5. visual/text Agent protocol translations and rejection conditions;
6. exact local protocols and the four arm classes;
7. residual hypotheses, alternative explanations and kill criteria;
8. readiness, license, H5 and information boundaries;
9. unranked branch portfolio and reproduction-first Stage-2A recommendation.

Run an independent exact-manifest review, resolve bounded defects without rewriting earlier audit,
then request `SIGN_STAGE1C_V2_FAMILY_BRANCH_PORTFOLIO`. After signature, freeze the Stage-1C release,
refresh HOT/CURRENT, verify archive safety and move eligible superseded unregistered work to the cold
layer. Do not push without separate publication authority.

## 11. Verification matrix

| Requirement | Authoritative proof |
|---|---|
| R2 intake integrity | exact receipts, prompt/model/process provenance, N=56 schema/semantic checks |
| calibration validity | frozen raw outputs, pre-adjudication per-path gates, disagreement/adjudication log |
| 320 coverage | exact-ID census: 56 carry-forward + 264 new = 320, duplicate/exit checks |
| experiment identity | cell/observation schemas, source locators, multi-metric and config-change tests |
| dataset graph | source-backed lineage tests and relation/lineage non-substitution checks |
| family validity | signature compatibility, typed membership and comparability-key tests |
| review | reproducible 64-paper sample plus 100% carrying-object review receipts |
| K/S/M attribution | one primary intervention per cell, combination/unresolved rules |
| branch gates | five-gate and four-arm machine validation |
| no execution | all local protocols `NOT_EXECUTED`; zero research/metric/reproduction/prototype flags |
| reproducibility | Windows/WSL deterministic regeneration, manifests, hashes, audit immutability |

## 12. Immediate next owner decision

The exact next token remains:

`AUTHORIZE_STAGE1C_V2_AGENTIC_CALIBRATION_R1_CODEBOOK_CONSOLIDATION`

It opens Phase A only. If the positive-support preflight proves that the unchanged source packet
cannot calibrate a mandatory object class, execution must stop and present a separate bounded repair
request rather than silently altering N=56 or source exposure.
