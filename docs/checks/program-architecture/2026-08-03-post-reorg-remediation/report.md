# Post-reorganization remediation — acceptance receipt (2026-08-03)

Remediation of `docs/superpowers/specs/2026-08-03-post-reorganization-architecture-review-and-remediation-proposal.md`
(`PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1`, verdict `CONDITIONAL_ACCEPT_WITH_REMEDIATION`).

## Transactions landed

| Transaction | Repo | Commits |
|---|---|---|
| T0 truth alignment (P0-1) | umbrella | `5fa2249` |
| T1 legacy resolution (P0-2) | umbrella | `e85ac82` |
| T1.5 checker upgrade / registry v2 (P1-3) | umbrella | `989ae98` |
| T4 snapshot provenance (P1-4) | study + umbrella tombstone addendum | study `4ceaba9`; umbrella (this commit) |
| T3 shared-code dependency ruling (P1-1) | study + umbrella guides | study `5dd1822`; umbrella (this commit) |
| T2 minimum engineering baseline (P1-2) | study | `ac75a61` |
| T5 common ownership audit (P2-1) + stale-spec supersession (P2-2) | umbrella | `5fa2249` (OWNERSHIP.md, spec status) |

Study repository: `audio-aware-evidence-acquisition`, HEAD `ac75a61` (local only — push requires
explicit authorization). Baseline reviewed commits: umbrella `772e6ed`, study `53d9283`.

## Section-13 rulings applied (user directive: implement the proposal)

1. Overall verdict accepted; all P0/P1 items remediated this transaction series.
2. T0–T3 confirmed as hard gates before first model touch — all closed.
3. Cold backups: GitHub remotes **plus** offline `git bundle` copies under
   `SPEECHRL_DATA_DIR/program-archives/` (SHA-256 registered in
   `docs/integrity/retired-repository-registry.json`).
4. `common`: no dependency while unconsumed (proposal §6.2.4); exact-commit pin policy recorded in
   the study migration manifest for first consumption.
5. Executed single-operator: umbrella T0/T1/T1.5 and study T2/T3/T4 in one reviewed session.

## Acceptance outputs (2026-08-03)

```text
== umbrella gates (Windows) ==
code graph: PASS (21 trusted nodes)
study workspace and experiment assets: PASS
study workspace and experiment assets: PASS [--require-installed]
legacy asset resolution: PASS {'WORKTREE_PRESENT': 0, 'LOCAL_GIT_HISTORY': 0,
                               'COLD_BACKUP_RESOLVED': 574, 'UNRESOLVED': 0, 'waived': 0}
AI context surface: PASS (0 failures)
AI context manifest: PASS
== checker unit tests (Windows) ==
136 passed, 2 skipped, 190 subtests passed
== common tests (WSL, Python 3.12 speechrl venv) ==
21 passed, 1 skipped
== study tests (WSL) ==
42 passed
== study build (WSL) ==
python -m build: sdist + wheel built; zero reference/w1-snapshot entries in either
uv lock: resolved 9 packages; uv sync --frozen dry-run resolves
```

## Residual items (non-blocking, owner discretion)

- Whether a second offline medium (beyond `SPEECHRL_DATA_DIR`) should hold the four bundles.
- Whether `--require-installed` becomes the default habit on the primary dev machine.
- `LEGACY_W_ERA` module physical shrink in `common/` — deferred to the post-R0 pass per T5 timing.
- Study CI has not run remotely (push withheld); it is exercised locally via the same commands.

R0-engineering-foundation-ready sign-off remains a team/owner action (proposal §13), not asserted
by this receipt.
