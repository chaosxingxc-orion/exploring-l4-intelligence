# MD and script consolidation campaign spec (2026-07-29)

## Authority

owner 2026-07-29 directive (sense by sense): clean up everything, including files inside the wiki,
CLAUDE.md, AGENTS.md, and the Markdown and related scripts inside the engineering repos.
**For Markdown, judge by content**: anything with no direct relation to the current work is removed
outright; weakly related material is summarized and then archived; only strongly related material is
kept. **For scripts, judge whether they are strictly required**: everything not required is deleted;
for those that are required, analyze further whether a template + configuration can optimize them,
reduce the script count, and turn them into configuration files. Supplementary ruling: **"In one
sentence: delete everything that should be deleted!"** — borderline items are deleted by default (the
ledger preserves recoverability), and only items bound to a gate or load-bearing as R2–R9 re-review
evidence are kept.

Definition of the current work (the grading baseline): Stage-1C R2–R9 opening-report-style
collaborative re-review (07-29 criteria and templates) → Stage-2A R5+R6+R8 vertical slice
(core = Qwen3-Omni-30B via llama.cpp, ASR main line = general ASR).

## Disposition rules

- MD: STRONG is kept (the current load surface, active proposals/templates, dossier/T1-T3 evidence,
  the HOT canon, README/CONTRIBUTING, gate-referenced files); WEAK first gets a 2-4 line summary
  merged into this campaign's digest and is then deleted into the ledger; NONE is deleted straight
  into the ledger. CLAUDE.md/AGENTS.md are not deleted but slimmed section by section (mirrored in
  sync, ≤12KB).
- Scripts: MUST_GATE (the 10 gates and their import closure) / MUST_INFRA (env/data/wiki-sync/train/eval
  entry points) / MUST_PYTEST (guarding active invariants) are kept; everything else, NOT_MUST, is
  deleted into the ledger. The MUST group produces a template + configuration convergence proposal
  (engine + declarative configuration); whether it is implemented is ruled on by the owner against
  that proposal.
- `wiki/audit/**` and `wiki/archive/**` are not touched by a single character. If a registered AUDIT
  artifact must be deleted, it goes through the registry sunset array (path/git_blob/last_commit, with
  history-reachability verification), reusing the 07-28 mechanism.

## Mechanism

- This campaign's audit directory: `wiki/audit/md-script-consolidation-2026-07-29/` — `sunset-ledger.jsonl`
  (reusing the 07-28 row schema, decided_by=owner-2026-07-29) + `sunset-digest.md` (WEAK summaries and
  the final state of each chain). The previous campaign's ledger debt of 143 scripts is backfilled into
  this campaign's ledger as `reason_class=SUNSET_TOOLING_BACKFILL`.
- At the close of each wave: if the current layer is involved, re-stamp the manifest + ai-context
  manifest + package receipt in the same commit; each wave commits and pushes after
  `sf_current_package_check.py --check` PASSes.
- Waves: A = umbrella wiki+docs MD; B = root MD plus the CLAUDE/AGENTS slimming; C = engineering-repo MD
  (each repo commits independently); D = script deletion + the 143 backfill; E = the configuration-driven
  proposal (a document, implemented separately after the owner rules on it).
- **scripts/tools/ (owner ruling 2026-07-29)**: establish a permanent directory holding the engineering
  tools used repeatedly day to day. The existing fetch/registration line (sf_fulltext_fetch,
  sf_fulltext_ledger_status, sf_official_metadata_fetch, sf_atom_provenance_fetch) moves in; a deleted
  discovery-track tool, if the R2-R9 re-review genuinely needs it, is restored on demand into this
  directory from its ledger recovery point. The move does not change the paths of the 10 gate-bound
  scripts (code_graph stability comes first); only day-to-day tools outside the gates go into tools/.

## Verification

After each wave's deletions: the 10 gates PASS, the load surface has no dangling references, and a
sample of deleted files is recoverable via `git show`. Inventory inputs: two parallel Opus grading
reports (MD grading / script necessity + configuration-driven design), executed after the main session
reviews them table by table.
