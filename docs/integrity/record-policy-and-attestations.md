# Record policy (hot/cold layering) + artifact attestations

Append-only. Seeded 2026-07-14 to discharge the reassessment
(`wiki/2026-07-14-response-to-precheck-doctoral-review-adversarial-reassessment.md`) §11.1-A
(hot/cold record-policy statement) and §11.1-B (post-commit artifact attestation).

## 1. Two-layer record policy (Decision-Log 续34; this note formalizes it)

Records are layered to reconcile three constraints — **append-only integrity**, **freshness**, and
**context economy / model focus** — without rewriting history:

- **Cold audit layer** (append-only, read on demand only, never rewritten): `wiki/Decision-Log.md`,
  `wiki/archive/**`, the dated `docs/integrity/*` registers, and every dated review/response/
  correction artifact under `wiki/`. Full history lives here; git preserves it.
- **Hot current layer** (small, curated, the default read): `wiki/Research-Objective.md` (single
  current-state entry point), `wiki/Per-Work-Status.md`, `CLAUDE.md`/`AGENTS.md`. Derived from the
  cold layer, reconstructable, **not the sole record of anything**; superseded items drop out so it
  stays bounded.

**Sequence rule**: a new decision is appended to the cold layer FIRST, then reflected into the hot
layer. Editing the hot layer is a derived-view refresh, NOT a rewrite of history.

**On the earlier "全程 append-only correction, 无覆盖旧文档" wording** (response `0be1285` §6): commit
`14943f1` edited an existing file (`wiki/2026-07-13-response-v6-correction.md` — softened a §3 header,
added the §3a normalization ledger). Under the strict old "everything append-only" reading that is
literally an in-place edit; under this layered policy it is a **hot-layer supplement** whose full
prior content is retained in git history (`git diff 14943f1^ 14943f1`). Classified as a
**policy-transition wording inconsistency**, not misconduct (reassessment §2.2 / Round 9 concur).

## 2. Standing provenance invariant (P0-REC-1, generalized)

Any record artifact published "to a reviewer / to the owner" MUST carry a split provenance triple in
frontmatter — never a single `snapshot` field:

- `evidence_snapshot`: the repo state the artifact reports on (umbrella + W1 commits).
- `artifact_snapshot`: the artifact's own `{path, umbrella_commit, sha256_git_blob}` — recorded here
  (or in a manifest) **after** commit, since a file cannot reliably contain its own hash.
- Canonical hash = git blob bytes (`git show <commit>:<path> | sha256sum`), never a working-tree
  read (CRLF variants do not reproduce from a clean clone).

## 3. Attestations (post-commit `(path, commit, blob-hash)` triples)

Verify any row with: `git show <umbrella_commit>:<path> | sha256sum`.

| artifact | umbrella_commit | sha256_git_blob |
|---|---|---|
| `wiki/2026-07-14-response-to-precheck-doctoral-review.md` | `0be1285e9242d195039b5fd3bc5425b1d741499c` | `7033539fed07906e534ad22844d4d9b864b560e3c884bbf75c3ed5157760136e` |
| `wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure-doctoral-review.md` | `25cffa9b06f7b36289b931bd6b73a8a8d4204542` | `cd56af0095d06b2e6197572e6e899e53ea460fde6625fe7f2b8a9f9eb0cbb3bf` |

(Both blob hashes were independently reconfirmed by the reassessment, which noted a PowerShell
UTF-8 pipe can produce a pseudo-hash — Python/`sha256sum` on the git blob is the canonical method.)
