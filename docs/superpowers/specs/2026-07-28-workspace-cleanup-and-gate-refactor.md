# Workspace cleanup and gate refactor — engineering spec

**Status: DRAFT — doc-side scope locked by owner rulings 2026-07-28; script-side dispositions
pending the gates-audit report.**
**Authority:** owner 2026-07-28 ("clean it all up" → "delete everything that should be deleted" →
"the scripts even more so — a systematic cleanup and refactor, so that as far as possible the
workspace is clean before large-scale analysis formally begins and the research direction is
locked").
**Campaign:** `workspace-cleanup-2026-07`. Inputs: three read-only inventory reports
(document disposition, audit-file sunset analysis, gates audit) produced 2026-07-28.

## 1. Scope and hard boundaries

In scope: working-tree deletion of superseded records with a blob-recoverable sunset ledger;
retirement of dead-campaign scripts; oracle strengthening of surviving gates; manifest/registry/
index machinery updates to keep every fail-closed check green.

Out of scope (hard boundaries, owner informed):

1. **No git history rewrite.** History purge would change every commit hash, including the
   canon-pinned Stage‑1B v5 `38fb9435d0c35e226ad62b16015a6dbee054e6c2` and all 110 registry blob
   anchors. "Delete" therefore means: remove from working tree; bytes remain reachable via
   `git show <commit>:<path>` and are indexed in the sunset ledger.
2. **14 retained wiki-root files are not deleted** (live canon claims rest on them): the four
   RETAIN_LOAD_BEARING files (W4 #29 proposal draft; W1 group-split statistics design;
   v10-consolidated as the B8-correction object; inherited-prior-exposure union) and the chain
   terminals (v42 external-review bytes + v42 signoff-refusal review; forensic REJECT-CLOSEOUT;
   recalibrated review that originated the 1A/1B/1C taxonomy; identity-contracts v1;
   knowledge-stack SHELVE-ALL response; owner-clarified pivot review; S0 identity signoff;
   v3-consolidated working-thesis baseline; round-11 v9 proposal + v9 review).
3. **Registered AUDIT transaction directories under `wiki/audit/` are untouched** except INDEX
   regeneration.

## 2. Deletion manifest (doc side — locked)

| Tier | Set | Count/size | Action |
|---|---|---|---|
| T1 | wiki-root SUNSET_SUPERSEDED files | 48 / 1.21 MB | delete + ledger |
| T2 | Stage‑1A rounds 1–10 non-terminal files (tight option; keep v3 + round-11 trio) | ~19 / ~0.5 MB | delete + ledger; INDEX rows keep verdicts + blob pointers |
| T3 | 07-15 selector-first proposal (was UNCLEAR) | 1 | fix Per-Work-Status phrase first, then delete + ledger |
| T4 | Retired precalibration workbench chain (RC2→R2R1, 6 campaigns) | 151 / 2.70 MB | delete + ledger |
| T5 | current-layer superseded data (free moves + script-gated after script retirement + rubric v1 pair after manifest/README edits) | 10 / ~236 KB | delete + ledger; manifest/prose edits in same commit |
| T6 | docs/checks root strays (pre-convention, unreferenced) + 5 dead check files + 3 unreferenced plans | ~48 / ~0.8 MB | delete + ledger; policy lane added to AI-Collaboration |
| Net | | ~270 files / ~5.4 MB | cold inventory 165 → ~40 paths |

## 3. Sunset ledger and registry model

- Ledger: `wiki/audit/workspace-cleanup-2026-07/sunset-ledger.jsonl` (AUDIT layer; append-only;
  registered on creation). One row per deleted path:
  `{path, bytes, git_blob, last_commit, tier, reason_class, decided_by: "owner-2026-07-28",
  retrieval: "git show <last_commit>:<path>"}`.
- Registry: rows are immutable → deletion is recorded by **appending** supersession records
  (`kind: "sunset"`, referencing the original artifact row) with the prefix count/hash anchor
  bumped in the same transaction, per AI-Collaboration §4.
- Checks learn one new rule: a registered path may be absent from the tree iff a matching sunset
  record exists (fail-closed otherwise).

## 3.5 Distill before delete (owner input 2026-07-28)

Deletion of narrative records is paired with distillation; raw bytes leave the tree, the
knowledge stays queryable:

- **`wiki/audit/workspace-cleanup-2026-07/sunset-digest.md`** — one compact digest (target
  ≤20 KB) written by an Opus pass that reads every T1/T2/T3 file and the T4 precalibration
  chain BEFORE deletion. Per chain (not per file): what was attempted / why it died /
  terminal verdict / lessons that carried into current canon / ledger pointers. Chains:
  pre-system-first era; 07-11 forensic audit; RDU v4.x; 07-13 recalibration+precheck;
  07-14 Survey-v2/P0-R/knowledge-stack; 07-15 pre-system-first proposals; Stage‑1A rounds
  1–10; precalibration RC2→R2R1 six generations.
- Every sunset-ledger row carries a one-line `summary` field (from the digest pass).
- T5/T6 (data files, mechanical check outputs) get ledger rows only — no narrative to distill.
- Decision-Log receives one ADR: cleanup decision, digest location, retrieval instructions.

## 4. Script side (locked from gates-audit report 2026-07-28)

Facts: no CI; the real gate = `sf_current_package_check.py` 18-command tuple + code_graph blob
pin over 175 .py files; full pytest ≈10.7 min with 86 RED; the retired stage1c-v2 cluster alone
costs 5.5 min; 5 collection errors come from verl's site-packages `scripts` package shadowing
(fix = importlib style in our files, never uninstall verl).

- **RETIRE: 55 files / ≈24,438 lines** (33% of scripts/) + `probe_hosts_c4a.sh`; headline: the
  closed stage1c-v2 subgraph (27 files / 14,402 lines), schema-v3 migrate/finalize (done,
  now RED), Stage-1B v3/v4 chain (v5 is canon), v4.2-era checkers, taxonomy v1–v4
  (**v5 stays — live import of v6**), one-shot receipt-frozen probes. Retirement commits must
  record the replay SHAs (`74cf8e4`, `7078623`, `8439295`) and regenerate
  `docs/checks/system-first-stage1a/context-v1/current-package-check.json` in the same
  transaction. Nothing under `wiki/audit/` or `docs/checks/` is deleted by this section.
- **STRENGTHEN: 13 files**; consolidation target ~110 prose-literal assertions → ~12 structural
  (endpoint as frontmatter token with cross-file equality; owner-rulings JSON with supersedes
  negation guard; router content = link-target set equality; delete zombie
  `ManifestRefreshPlanContractTests` with its stale 78-row pin; behaviour-not-source assertion
  for the rubric manifest check). `test_sf_r1_problem_definition.py` (77% weak, 0 negative
  tests, pins superseded Qwen2.5-Omni-7B) gets its stale pin fixed now; full JSON-contract
  promotion lands with the step-2 R1 rewrite.
- **TRIAGE FIRST (possible real defects, not drift):** `test_sf_proposal_package_check`
  ('PASS' != 'FAIL' — possible oracle inversion), `test_sf_reviewer_proposal_check`
  (`BIBLIOGRAPHY_NUMERIC_DRIFT` never raised — drift detector may be dead),
  `test_sf_archive_candidates` (fixture drift on a live gate member). Investigate before the
  non-cluster retirements.
- **KEEP set is NOT final (owner ruling 2026-07-28): code_graph pinning ≠ genuine need.**
  The 134 KEEP files undergo zero-based justification; a file survives only under one of:
  N1 = 18-command gate member guarding an invariant that can still change (frozen-blob
  integrity is already covered by immutability prefix hashes → per-frozen-artifact contract
  tests are ballast, RETIRE_WITH_GATE_EDIT); N2 = canon-referenced operational tooling;
  N3 = machinery this cleanup depends on (manifest/registry/immutability trio + true deps);
  N4 = needed by step-2/3 research work (fulltext fetch/registration/ledger pipeline,
  dataset/model fetch+verify incl. the Qwen3-Omni GGUF lane, asset inventory). Everything
  else retires; frozen receipts stay replayable from recorded commits.
- **Base+config consolidation (owner ruling 2026-07-28):** survivors are refactored toward a
  generic contract engine + per-artifact declarative config (schema ref, hash bindings,
  cross-file invariants, negation guards), canon-pin tests collapse to the structural-invariant
  design in this section, and the fetch-*.sh family consolidates into a lock-file-driven
  `fetch-candidates.sh`. Migration keeps the gate green at every commit. Shell:
  `fetch-candidate-{datasets,models}.sh` → MERGE_INTO `fetch-candidates.sh`;
  `lean_axiom_gate.sh` flagged to owner (wire or retire).

## 5. Execution order (one coherent package; each commit leaves checks green)

1. Script retirement (Sonnet) — unblocks script-gated file deletions.
2. Machinery extension (Sonnet): sunset-record support in registry/checks + ledger writer.
3. Distillation pass (Opus, §3.5) — sunset digest + ledger summaries, BEFORE any deletion.
4. Doc deletions T1–T6 with ledger rows; INDEX/campaign-index regeneration; manifest updates
   (current manifest gap: 22+ unlisted files registered or deleted; cold inventory prune).
5. Routing text cleanup (Opus): Per-Work-Status phrase, AI-Collaboration policy lane additions
   (docs/checks and plans retirement lanes), exposure-union path pin.
6. Oracle strengthening (Sonnet) per §4 STRENGTHEN list.
7. Full suite + surface checks green; grouped commits (scripts / machinery / deletions / policy /
   gates); final verification of blob recoverability for a sample of deleted paths.

## 6. Invariants (verified after every phase)

- All fail-closed checks pass; no partial/both-path states.
- Stage‑1B v5 hash and audit blob anchors unchanged.
- Every deleted path has a ledger row whose `git_blob` matches `git show` output.
- HOT/CURRENT files contain no dangling references to deleted paths.
- Research-Objective ≤5120 bytes; current README/status ≤4096 bytes; manifest ≤30 active entries.
