

---

## ⚠ Coordinator data-recount correction (2026-07-14, pre-commit — supersedes the numbers above where they differ)

Machine recount directly from `paper_works.jsonl` (95 rows) — the build agent's summary
overstated two numbers; the DATA rows are authoritative:

- identity_resolved: **94** / identity_unresolved: **1** (W-0014 morbini2012 — row honestly carries
  status=IDENTITY_UNRESOLVED, no canonical ID filled; MUST NOT be counted resolved)
- versions pinned (latest_version AND version_date non-empty): **83/95** (not 94/95)
- id-type distribution (recounted): {'venue_native': 5, 'arxiv': 83, 'doi': 6, 'NONE': 1}
- authors_full coverage: 95/95 (confirmed)
- candidate_works=95, source_clusters=94, P-0016 split, P-0084=NUMERIC_FINGERPRINT_TABLE3 (confirmed)

Lesson applied: headline numbers must come from machine recounts of the data files, never from
build-agent prose (third re-review, do_not_claim discipline). Status remains CENSUS_V2_SINGLE_PASS_AI,
human double-review pending; W-0014 stays out of any exact-works count.
