# Canonical Census v1 — SURVEY-RESP-2026-07-14-01

**Status token: `CENSUS_V1_SINGLE_PASS_AI`**

- Source: `wiki/survey/replay/SURVEY-RESP-2026-07-14-01/papers.jsonl` (94 record clusters; source file NOT modified)
- Records: [`census_records.jsonl`](census_records.jsonl) (this directory; 94 lines, one JSON record per cluster, sorted by `paper_id`, fields exactly as received from resolution)

## 1. P0-R2 acceptance counts (SEPARATE numbers — never aggregated)

| P0-R2 count | Value | Definition |
|---|---|---|
| `record_clusters` | **94** | rows in source papers.jsonl = rows in census_records.jsonl |
| `identity_resolved_works` | **92** | records with `status=RESOLVED` |
| `ambiguous` | **2** | records with `status=AMBIGUOUS` (P-0016, P-0084) |
| `identity_unresolved` | **0** | records with `status=IDENTITY_UNRESOLVED` |
| `versions_pinned` | **36** | records with non-empty `latest_version` AND non-empty `version_date` |
| `resolved_unique_works` | **92** | unique works among RESOLVED records after arxiv_id/DOI collision merge (see §2) |

These are distinct quantities and must be cited separately; in particular
`record_clusters (94) ≠ identity_resolved_works (92) ≠ versions_pinned (36)`.

Confidence distribution (all 94 records):

| Confidence | Count | paper_ids |
|---|---|---|
| HIGH | 87 | all except the 7 below |
| MEDIUM | 6 | P-0016, P-0030, P-0075, P-0076, P-0077, P-0078 |
| LOW | 1 | P-0084 |

Versions pinned (36): P-0005, P-0008, P-0022, P-0025, P-0026, P-0027, P-0029, P-0031, P-0032,
P-0034, P-0035, P-0036, P-0037, P-0038, P-0039, P-0040, P-0042, P-0045, P-0047, P-0048, P-0052,
P-0066, P-0068, P-0069, P-0070, P-0072, P-0073, P-0085, P-0086, P-0088, P-0089, P-0090, P-0091,
P-0092, P-0093, P-0094.
(Records with only one of `latest_version` / `version_date` non-empty — e.g. P-0004 v2 without a
date, P-0062/P-0075/P-0076/P-0081/P-0082 date without a version tag — are NOT counted as pinned.)

## 2. Cross-cluster collision check (merge candidates)

Checked every pair of paper_ids for resolution to the same `arxiv_id` or the same `doi`
(case-insensitive), across all 94 records:

- Non-empty `arxiv_id` values: 82 — **all distinct, 0 collisions**
- Non-empty `doi` values: 11 — **all distinct, 0 collisions**
- **Merge candidates: none.**

Therefore `resolved_unique_works = 92` = `identity_resolved_works` (no two RESOLVED records
share an arXiv id or DOI). True unique works may still be fewer than 94 record clusters: the two
AMBIGUOUS clusters are excluded from the exact unique-work count per P0-R2, and P-0016 is itself a
two-paper cluster. Records without any arXiv id/DOI (venue-only identities, e.g. ISCA/ACL-Anthology
pages) were not collision-checkable beyond their distinct canonical URLs; no duplicates were
observed among them, but this is a single-pass observation, not a verified guarantee.

Sibling near-misses inspected and confirmed as DISTINCT works (not collisions): P-0008 vs P-0009
(same first author Mingda Li, different papers/venues); P-0024 (2409.01160) vs P-0025 (2409.01201)
(same team, adjacent arXiv ids, different papers).

## 3. IDENTITY_UNRESOLVED and AMBIGUOUS rows (NOT counted in exact unique works, per P0-R2)

IDENTITY_UNRESOLVED: none.

| paper_id | ledger_key | status | confidence | notes |
|---|---|---|---|---|
| P-0016 | `ng2015-2016-slt-qe-kbest` | AMBIGUOUS | MEDIUM | Alias literally spans TWO distinct works by the same Sheffield team (Ng, Shah, Specia). Candidate A (reported in record): "Groupwise learning for ASR k-best list reranking in spoken language translation", ICASSP 2016 (DOI 10.1109/ICASSP.2016.7472853). Candidate B: "Quality estimation for ASR k-best list rescoring in spoken language translation", ICASSP 2015. Both real; which is canonical is ambiguous. Neither has an arXiv. |
| P-0084 | `KIT-IWSLT2026` | AMBIGUOUS | LOW | Alias carries no disambiguator; KIT made at least two distinct IWSLT 2026 arXiv submissions. Candidate A (leading, kill-I4 fit): "Multilingual Long-Form Speech Instruction Following: KIT's Submission to IWSLT 2026" (arXiv:2606.04730, 2026.iwslt-1.16). Candidate B: "KIT's Submission to Cross-Lingual Voice Cloning in IWSLT 2026" (arXiv:2606.07240, 2026.iwslt-1.8). Cannot resolve without the survey row's full-text context; no title/author/ids committed in the record. |

Both rows are retained in `census_records.jsonl` (they count toward `record_clusters=94`) but are
excluded from `identity_resolved_works` and `resolved_unique_works`.

## 4. Provenance

- Generated **2026-07-14** by the **canonical-census-v1** workflow (P0-R2 census merge step).
- Resolution method: **single-pass AI web resolution** (WebSearch/WebFetch against arXiv, ACL
  Anthology, ISCA Archive, IEEE Xplore, ACM DL, PMLR, OpenReview, and author/lab pages), one
  resolution record per cluster.
- **Human double-review is pending (P1).** This census is NOT claimed to be verified and NOT
  claimed to be complete; all counts above are acceptance counts of the single-pass resolution
  only, and every field inherits single-pass evidence grade. Known single-pass limitations are
  recorded per-row in `notes` (blocked WebFetches, unread version tags/dates, uncaptured author
  lists, DOIs left blank rather than invented).
- Status token: **`CENSUS_V1_SINGLE_PASS_AI`**
