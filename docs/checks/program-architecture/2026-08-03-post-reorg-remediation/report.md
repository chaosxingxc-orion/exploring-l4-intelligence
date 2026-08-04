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

- ~~Whether a second offline medium (beyond `SPEECHRL_DATA_DIR`) should hold the four bundles.~~
  **Ruled 2026-08-03 (owner, in-session): the E drive is the only storage medium; the bundles under
  `SPEECHRL_DATA_DIR/program-archives/` are the accepted default (and only) offline copy, alongside
  the GitHub cold-backup remotes.**
- ~~Whether `--require-installed` becomes the default habit on the primary dev machine.~~
  **Ruled 2026-08-03 (owner, in-session): adopted as the primary-dev-machine default; recorded in
  the client guides.**
- `LEGACY_W_ERA` module physical shrink in `common/` — deferred to the post-R0 pass per T5 timing.
- Study CI has not run remotely (push withheld); it is exercised locally via the same commands.

R0-engineering-foundation-ready sign-off remains a team/owner action (proposal §13), not asserted
by this receipt.

## Addendum (2026-08-03): four-round adversarial self-check

Owner-directed adversarial self-review of the remediation itself; converged after four rounds.

- **R1 — mechanical refutation sweep** (stale-truth grep over every active surface). Found and
  fixed: four live install instructions still showing `uv pip install -e ../../common -e .`
  (README, README_CN, docs/setup.md, wiki/Environment-and-Setup.md), three gate lists missing the
  new `legacy_asset_resolution_check` (README, README_CN, wiki/Onboarding.md), two stale CONTRIBUTING
  claims (W1–W4 "deleted" wording; `common` "editable-installed by admitted studies"), missing
  `shared code revision` column in the study experiment ledger header. Ruled untouched as
  append-only/dated history: `release_manifest.json`, `remediation_evidence.yaml`,
  `prior_exposure_registry.json`, `requirements-freeze-2026-07-09.txt`, decision-log volumes,
  historical spec quotes.
- **R2 — independent data re-verification** (fresh code path, not the generator). 574/574
  resolution entries re-proven against the mirrors (commit contains path, git blob equal, URI
  well-formed; exactly 1 resolves at a non-final commit — the historically deleted
  `_repro/wave1_results.md`, as expected). Claim-ledger URIs 17/17 resolvable after fixing one
  line-anchor glued into a URI (`...experiment_inventory.md:86` → `... line 86`). SNAPSHOT.md
  13/13 rows = SHA256SUMS = on-disk hashes. All four bundles: SHA-256 matches the registry,
  `git bundle verify` passes, mirror tips equal the frozen final commits.
- **R3 — fault injection** (temporary worktree, eight injected drifts): admitted-count drift,
  decision-record tamper (blob drift), resolution row removal (two distinct failures), unwaived
  UNRESOLVED, unregistered study directory, frontmatter namespace drift, missing checkout under
  `--require-installed` — **8/8 caught fail-closed**, baselines green.
- **R4 — semantic re-read + full acceptance re-run** — no new findings; suite green (outputs below
  supersede the first-pass table where they differ only by the R1/R2 fixes).

