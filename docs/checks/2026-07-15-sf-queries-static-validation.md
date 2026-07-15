# Gate S1 — SF query compiler static validation report (P0-B)

**Scope**: offline, network-free compilation of the 48 pre-registered SF-L1..SF-L8 arXiv
exact-query fragments (§4 of the Gate S1 retrieval protocol) into the frozen JSONL artifact
`wiki/survey/2026-07-15-sf-queries.jsonl`. This report documents the compiler run that produced
that artifact and the static (no-network) validation it passed. This is protocol
**compilation**, not retrieval execution — `queries_executed` remains 0.

## Inputs / outputs / provenance

| Role | Path | sha256 |
|---|---|---|
| Protocol source (parsed) | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `b217fbc080cf90874ffa6cad1ec69af579b1e1278ba355ba2b0b749371959fe7` |
| Compiler script | `scripts/survey/sf_query_compiler.py` | `b3f9d369fc5fca5c8b6baf30a9a2d232cf8b24921926fb5e1f887872189bea10` |
| Compiled artifact (output) | `wiki/survey/2026-07-15-sf-queries.jsonl` | `72674bfead4bdd29874f4318293637b047cc220c7fff65a157f990a7f5323e95` |

sha256 computed over the raw file bytes on disk (`hashlib.sha256(open(path,'rb').read())`);
these are Windows-checkout byte hashes at compile time — if the file is later checked out
through git normalization (`.gitattributes` forces `eol=lf` for `*.md`/`*.json`/`*.py`, and the
generic `* text=auto eol=lf` fallback for `*.jsonl`), the canonical git-blob hash is the one to
cite going forward (`git show <commit>:<path> | sha256sum`), consistent with this repo's
canonical-hash convention.

## Run command and environment

```
python scripts/survey/sf_query_compiler.py
```

Run from the umbrella repo root (`D:\chao_workspace\exploring-l4-intelligence`) using the
Windows system Python resolved by `python` on `PATH`:

```
Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
```

No project venv / no `torch`/ML stack needed — the compiler imports only
`hashlib`, `json`, `re`, `sys`, `collections.OrderedDict`/`collections.defaultdict`,
`datetime.datetime`, `pathlib.Path`, `urllib.parse.quote`. None of these modules are capable of
issuing a network request (`urllib.parse` is a pure string-manipulation submodule; the compiler
never imports `urllib.request`, `http.client`, `socket`, `requests`, `ftplib`, or any other
networking-capable module).

**Network requests made during compilation: 0.** This is a protocol *compiler* — it parses a
local markdown file and writes a local JSONL file; it performs no HTTP calls, no DNS lookups, no
sockets of any kind, attested both by code inspection (import list above) and by the nature of
the task (pure string processing over an already-local file).

Exit code of the run: **0** (all checks passed — see below).

## Parse result

- Parsed **48** `- Q<n> \`...\`` Boolean query fragments from §4, across lanes `SF-L1`..`SF-L8`
  (6 each), matching the frozen scope (`8 lanes × 6 = 48`).
- The protocol document was found to contain one additional §4 subsection outside compiler scope,
  **`SF-L9`** ("foundational lineage" lane, added by an in-flight `amendment-1` to the protocol
  document — see "Mid-task source-document amendment" below). It was verified to carry **zero**
  `- Q<n>` Boolean query lines (the protocol text explicitly states this lane has "无预注册
  Boolean 查询" / uses backward/forward chaining from DOI-anchored classics instead, and is
  statistically isolated from the 2022–2026 novelty pool). The compiler treats any non-`SF-L1..8`
  lane as out-of-scope **only if** it has zero Boolean query lines; had `SF-L9` contained any
  `- Q<n>` line, the compiler would have hard-failed rather than silently drop it. Excluding
  `SF-L9` from the 48-query compilation causes no loss of in-scope content and is consistent with
  the live document's own `§4` heading ("八条 lanes") and its own restated total ("48 条编译冻结
  arXiv 查询").
- No parse warnings; no fabricated records.

## Static validation results (all network-free, string/structure checks only)

| Check | Result | Details |
|---|---|---|
| `row_count_equals_48` | PASS | got 48 |
| `query_id_unique` | PASS | n_unique=48 |
| `no_placeholder_or_ellipsis_or_angle_bracket_residue` (no CJK conditional-placeholder text, no `…`/`...`, no `<`/`>` residue) | PASS | clean |
| `no_stray_brackets_outside_submittedDate` (`[`/`]` only legitimate inside `submittedDate:[...]`) | PASS | clean |
| `balanced_parens_and_quotes` | PASS | clean |
| `boolean_operators_fully_uppercase` (AND/OR/ANDNOT, with quoted natural-language phrases such as `abs:"reasoning and acting"` masked out first so their embedded lowercase "and" is not misidentified as an operator) | PASS | clean |
| `dates_well_formed_and_ordered` (`%Y%m%d%H%M`, `date_from <= date_to`) | PASS | clean |
| `each_lane_has_exactly_6_queries` | PASS | all lanes=6 |
| `bonus_categories_match_frozen_mapping` (extra, not part of the requested check list) | PASS | clean |
| `bonus_exceptions_applied_correctly` (date/max_results exceptions land exactly on `SF-L2-Q3`/`SF-L3-Q3`/`SF-L7-Q3` and nowhere else) | PASS | clean |
| `bonus_record_sha256_recomputes_identically` (per-row hash self-consistency) | PASS | clean |

**OVERALL: PASS (0 failures / 11 checks, 8 required + 3 bonus)**

## Compiled assembly spec applied (verbatim from task instructions)

- Category expression:
  - `SF-L1`/`SF-L2`/`SF-L4`/`SF-L5` → `cat:cs.CL OR cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.RO`
  - `SF-L3` → the above five plus `OR cat:cs.SD OR cat:eess.AS`
  - `SF-L6`/`SF-L7`/`SF-L8` → `cat:cs.CL OR cat:cs.AI OR cat:cs.LG`
- Date window (double-closed): default `202210010000`–`202607152359`; exceptions
  `SF-L2-Q3`/`SF-L3-Q3` → `date_from=202301010000`; `SF-L7-Q3` → `date_from=202001010000`
  (`date_to` unchanged in both exception cases).
- Pagination: `start=0`, `max_results=75` (`SF-L7-Q3` → `max_results=50`); overflow/full-paging
  rule is out of scope for this compiler (governed by the protocol's separate amendment text) and
  is not represented in the compiled record.
- `sortBy=relevance`, `sortOrder=descending`.
- Final template: `(<category expression>) AND submittedDate:[<from> TO <to>] AND (<Q fragment>)`.

Verified spot checks (see the JSONL for full records):

- `SF-L2-Q3`: categories = 5-cat set, `date_from=202301010000`, `max_results=75`.
- `SF-L3-Q3`: categories = 7-cat set (+`cs.SD`/`eess.AS`), `date_from=202301010000`, `max_results=75`.
- `SF-L7-Q3`: categories = 3-cat set, `date_from=202001010000`, `max_results=50`.

## Mid-task source-document amendment (transparency note)

While this compiler task was in progress, `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md`
was modified on disk (uncommitted, presumably by a concurrent session working the paired `P0-A`
remediation track against the same doctoral-review findings — see commit `5ca99bf` "Gate S1
protocol RETURNED FOR MAJOR REVISION"). The live document now:

1. Widens the category mapping for `SF-L1`/`SF-L2`/`SF-L4`/`SF-L5` to include `cs.CV`/`cs.RO`
   (verbatim match to the category-expression spec given to this compiler task).
2. Adds a 9th lane, `SF-L9` ("foundational lineage"), explicitly carrying zero pre-registered
   Boolean arXiv queries and statistically isolated from the 2022–2026 novelty pool.
3. Already contains prose (§4, "exact-query 冻结正典") describing this very compiler, this very
   JSONL artifact path, and this very validation-report path as the intended deliverables —
   i.e. the concurrent session had already written forward-referencing documentation expecting
   this task's output. Field names and paths in that prose match this deliverable exactly.

None of this changed the compiled scope or count (still `SF-L1..SF-L8`, 48 queries); it is
recorded here only so a reviewer knows the source file was a moving target during compilation and
which byte-content (hash above) was actually parsed.
