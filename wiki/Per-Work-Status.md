# Per-Work Status

> Targeted secondary view; default current-state entry is `wiki/Research-Objective.md`.
> Last refreshed 2026-08-25. Historical narration is cold: start from the campaign index or
> `wiki/archive/`, then use targeted search. Literature work routes through
> `wiki/survey/README.md`.

## Program study pipeline

- **Carrier:** the umbrella program and its Wiki; W1 is no longer the primary-program carrier.
  Carriers bind stages (Decision-Log continuation entry 91): Stage‑1 = umbrella,
  Stage‑2 = `studies/<slug>`, Stage‑3 = `papers/<slug>`.
- **Repository rule:** admitted research objects use independent semantic GitHub repos under
  `studies/` and `papers/`. Candidate IDs remain audit provenance and never become engineering
  names. R1 sunset before admission, so it has no repo. `studies/registry.json` holds one admitted
  study and `papers/registry.json` one admitted paper project.
- **Admitted study:** speech-aware evidence acquisition (source-candidate provenance R2).
  `OWNER_GO_AND_EXECUTION_CONTRACT` signed 2026-08-03; speech-only scope/identity effective
  2026-08-04; repo `studies/speech-aware-evidence-acquisition/` (private remote) with the freeze sheet
  in `wiki/experiments/speech-aware-evidence-acquisition/`. General/environmental audio is excluded;
  local downloaded bytes are retained globally. Innovation converges in Stage‑2; the study ends at
  qualified paper candidates.
  Stage-2A is in flight under a standing GO: model-free E0 (D1–D4) and the runtime receipt closed
  2026-08-04, the R0 engineering baseline landed 2026-08-05, `SAEA-E-001` completed 2026-08-09 with the
  R0 measurement-integrity exit criterion met, and the knowledge-plane baseline was locked 2026-08-25
  with a second carrier opened at mechanics-and-first-signal scope only. Verdicts and figures are
  canonical in `wiki/Research-Objective.md` and
  `wiki/experiments/speech-aware-evidence-acquisition/README.md` and are not copied here. A
  Stage-2B qualification-freeze candidate is drafted and still awaits an owner decision.
- **Admitted paper project:** `papers/meeting-minutes-agent/` (2026-08-17, status `ACTIVE`, private
  remote; authorization record
  `wiki/experiments/papers/meeting-minutes-agent/2026-08-17-owner-go-and-paper-execution-contract.md`).
  It entered by **direct owner admission**, superseding the promote-from-a-qualified-study-candidate
  default of continuation entry 91 **for this object only**; the default stands for every future
  admission. Same-session cross-carrier scope ruling: meeting-notes-class corpora and the interleaved
  listening/spelling/revising scheme belong to this paper project, while knowledge injection stays with
  the study on non-meeting data. Continuation entry 92's trigger fired with this admission, so
  `scripts/checks/paper_workspace_check.py` now runs in admission mode.
- **Paper-scale stop line (continuation entry 91):** production-scale confirmatory work, final
  superiority or generality claims and manuscripts require an admitted `papers/<slug>` repo via
  `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` — never a study repo.
- **Flow:** an admitted object may enter engineering while the next candidate is surveyed; R3–R9
  review is not a global prerequisite. D0 acquisition is closed for Earnings21, Earnings22 and ConEC.
  Model/tool contact is gated by a structured `ExecutionPlan` and mandatory exposure pre-registration,
  not by numeric budget bands: the first-slice call/GPU-hour/audio-hour caps were retired by the
  2026-08-06 owner amendment, while paid API spend = 0 and one-shot attempt semantics remain
  machine-enforced. Publication and the Wiki mirror remain closed today.
- **Assets:** `wiki/Experiment-Assets.md` is the management router. The legacy 574-row W1 attempt
  inventory is fully resolved against the retired cold-backup remotes (574 `COLD_BACKUP_RESOLVED`,
  0 unresolved) via `docs/integrity/legacy-asset-resolution.json` and the retired-repository
  registry; offline git bundles of all four retired repos live under
  `SPEECHRL_DATA_DIR/program-archives/` with registered SHA-256, verified bundle-side.

## W1

- **Retired 2026-08-03:** `speech-mllm-training-free-rl` retired by owner ruling (historical residue);
  local checkout deleted, remote kept as a cold backup unlinked from the program. Thirteen rescued
  files live in the admitted study's `reference/w1-snapshot/` (ten at source commit `7ed41f62`, two
  best-of-N runners at `28d8f0d`/`f9d111a`, `gpu_session.sh` at `7ed41f62`).
- **Surviving boundary:** Stage‑1B v5 `38fb9435d0c35e226ad62b16015a6dbee054e6c2` and the 320-work union
  remain fixed evidence. R1 agreement remains `FAIL`; R2R1 remains
  `RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`; H5 remains withheld and non-load-bearing.
  The program-level Stage‑1B Lean layer is retired; formal work is rebuilt per admitted study in
  Stage‑2.

## W2

- **Retired 2026-08-03:** `speech-mllm-efficient-rl-alignment` (supporting skeleton) deleted; final HEAD
  `766bbc9`; its uncommitted config-default tweak is recorded in the tombstone.

## W3

- **Retired 2026-08-03:** `speech-mllm-multitask-rl` (supporting skeleton) deleted; final HEAD `931806c`;
  its uncommitted config-default tweak is recorded in the tombstone.

## W4

- **Retired 2026-08-03:** `speech-mllm-omni-embedding-rl` deleted; final HEAD `0f587c6`. Historical
  probes stay citable through Git history and the tombstone only; the ticket #29 proposal lapses.

## Shared boundaries

- North star: `wiki/Project-Thesis.md`; current stage and blockers: `wiki/Research-Objective.md`.
- Admitted-object code belongs in its independent semantic repo; umbrella records and both registries
  (`studies/registry.json`, `papers/registry.json`) belong here. Retirement record:
  `wiki/archive/program/w1-w4-retirement/`.
- Historical per-work detail is not repeated. Resolve it from its cold campaign index or `wiki/archive/`
  only for a named provenance question.
