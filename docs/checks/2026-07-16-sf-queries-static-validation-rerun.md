# Gate S1 — SF query compiler static validation RERUN report (A3-8, P0-B)

**Scope**: offline, network-free re-compilation of the SF query set after amendment-3's A3-8
registered addition (3 further exact-query fragments, append-only) to §4 of the Gate S1 retrieval
protocol: `SF-L1` gains `Q7`/`Q8`, `SF-L3` gains `Q7`. Expected query set = original **8 lanes ×
Q1..Q6 (48)** + **3 registered A3-8 additions** = **51**. This report reruns the full static
validation performed by `docs/checks/2026-07-15-sf-queries-static-validation.md` (adjusted to the
51-query scope) and adds three new checks the A3-8 upgrade specifically requires:

1. the 48 original records are **byte-for-byte unchanged** (prefix invariance) — the additions
   must be strictly appended, never touch the original 48;
2. the 3 addition rows carry correct `query_id` / `lane` / `compiler_version` fields;
3. the compiler's guard against an **unregistered** `Q>=7` line silently entering the compiled set
   actually exists and fires.

This is protocol **compilation**, not retrieval execution — `queries_executed` remains **0**.
**Network requests made during this rerun: 0** (see "Run command and environment" below).

## Relationship to the original report (differences)

- The original report (`2026-07-15-sf-queries-static-validation.md`) is **not superseded content**
  — it is left as the historical record of the pre-A3-8, 48-query compile. This report **takes
  over its "protocol → compiler → jsonl" chain-of-custody proof role going forward**: the original
  report's cited protocol input sha256 (`b217fbc080cf90874ffa6cad1ec69af579b1e1278ba355ba2b0b749371959fe7`)
  is now **stale** — the live protocol document has since been amended (amendment-3 / A3-8, and
  earlier concurrent-session edits already disclosed in the original report's own "Mid-task
  source-document amendment" section) and no longer hashes to that value. This report recomputes
  and cites the **current** protocol / compiler / jsonl sha256 triple as the live chain-of-custody
  evidence.
- Compiler script changed (`scripts/survey/sf_query_compiler.py`): added an `ADDITIONS` registry
  (`{"SF-L1": [7, 8], "SF-L3": [7]}`), a two-tier `compiler_version` (`sfqc-1.0.0` for the 48 base
  records, unchanged; `sfqc-1.1.0` for the 3 addition records), a hard-fail guard for any
  unregistered `Q>=7` line, and an explicit base-then-additions output ordering. See diff summary
  in "Compiler changes" below.
- Output artifact (`wiki/survey/2026-07-15-sf-queries.jsonl`) grew from 48 to **51** lines; the
  first 48 lines are asserted byte-identical to the pre-A3-8 (git `HEAD`) version — see check ①.
- Validation check set grew from 11 (8 required + 3 bonus) to **13** (8 required, re-scoped to 51
  rows / per-lane counts that now vary by lane + 5 bonus, 2 new: version-tiering and
  order-prefix), run **inside** the compiler script, **plus 3 further checks done at
  report-compilation time** (external to the compiler's own `main()`, since they require comparing
  against `git show HEAD:...` and running the parser against synthetic injected text — the compiler
  itself has no git dependency and no reason to synthesize malformed input against itself).

## Inputs / outputs / provenance (current chain-of-custody triple)

| Role | Path | sha256 (current, raw file bytes) | bytes |
|---|---|---|---|
| Protocol source (parsed) | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `db3068982f9ca1a0ff657cb924c491d034b6302f6b557af1e5698b1bc1ca6413` | 39431 |
| Compiler script (A3-8 upgraded) | `scripts/survey/sf_query_compiler.py` | `3f37b5262cba99d5e7c5a239179ae4a5dbad22644bf24824eb8f127420c7e80d` | 24157 |
| Compiled artifact (output, 51 rows) | `wiki/survey/2026-07-15-sf-queries.jsonl` | `4e40658010d89833878e1f353a4975db5f86a52547f0fd10adbf093cf054a5e9` | 49655 |

sha256 computed over raw file bytes on disk (`hashlib.sha256(open(path,'rb').read())`), same
convention as the original report. These are the **current working-tree** hashes at the time this
rerun report was written — i.e. "current protocol → current compiler → current jsonl" is a
self-consistent, freshly-verified chain: the compiler above was executed against the protocol
above and produced exactly the jsonl above (re-verified live during this report's authoring, not
carried over from a prior run).

Repo HEAD at time of this rerun: commit `705b69a84cd4305a91e1ccc9896c60bbc79a7387` (2026-07-15
23:22:25 +0800). Note the protocol file, seed manifest, and several other `wiki/` files show as
modified in the working tree relative to this HEAD — this is **pre-existing, concurrent-session**
state (per this repo's own "concurrent sessions coordination" convention), not something this task
touched; this task's edits are confined to exactly the 3 files named in its own instructions
(`scripts/survey/sf_query_compiler.py`, `wiki/survey/2026-07-15-sf-queries.jsonl`, and this report).

## Run command and environment

```
python scripts/survey/sf_query_compiler.py
```

Run from the umbrella repo root (`D:\chao_workspace\exploring-l4-intelligence`):

```
Python 3.14.3
```

(same interpreter as the original report's run — Windows system Python resolved by `python` on
`PATH`; no project venv / no ML stack needed). Import list is unchanged from the original report's
attestation: `hashlib`, `json`, `re`, `sys`, `collections.OrderedDict`/`collections.defaultdict`,
`datetime.datetime`, `pathlib.Path`, `urllib.parse.quote` — none capable of a network request.

**Network requests made during this rerun: 0.** Attested by (a) code inspection — the A3-8 upgrade
added zero new imports, only the `ADDITIONS` registry, two version constants, and pure
string/dict logic; (b) the nature of the task — parsing a local markdown file and writing a local
JSONL file. **联网检索查询执行数 = 0**（attestation，与协议 frontmatter `queries_executed: 0`
口径一致；本次任务全程零 arXiv/Semantic Scholar/OpenAlex 等外部检索调用）。

Exit code of the run: **0**. Wall-clock time (measured via `time -p` around the same invocation
shown above): **real 0.10s** (user 0.00s, sys 0.01s).

## Parse result

- Parsed **48** base `- Q<n> \`...\`` fragments from §4 (`SF-L1..SF-L8`, Q1..Q6, 6 each) **plus 3**
  A3-8 registered additions: `SF-L1-Q7`, `SF-L1-Q8`, `SF-L3-Q7` — total **51**.
- `SF-L9` ("foundational lineage") remains out-of-scope with **zero** Boolean query lines, exactly
  as in the original report — unaffected by A3-8.
- No parse warnings; no fabricated records.

## Compiler changes (A3-8 upgrade summary)

- New `ADDITIONS = {"SF-L1": [7, 8], "SF-L3": [7]}` registry — the single sanctioned source of
  which lanes may carry Q-numbers beyond the base Q1..Q6.
- `expected_q_nums_for_lane(lane_id)` = base `[1..6]` + `sorted(ADDITIONS.get(lane_id, []))`; each
  lane's parsed Q-numbers are checked against this set. Any `- Q<n>` line whose number is neither a
  base number nor a number registered in `ADDITIONS` for that lane is a hard `ParseError` (exit 1)
  — see check ③ below for empirical proof this fires.
- `COMPILER_VERSION` (single constant) replaced by `COMPILER_VERSION_BASE = "sfqc-1.0.0"` and
  `COMPILER_VERSION_ADDITIONS = "sfqc-1.1.0"`; `assemble_record()` tags each record via
  `is_addition_query(query_id)` (looks the query's lane + Q-number up in `ADDITIONS`), so the base
  48 keep `sfqc-1.0.0` unconditionally and only the 3 registered additions get `sfqc-1.1.0`.
- `parse_all_queries()` now returns `(base_queries, addition_queries, out_of_scope_lanes)` instead
  of a single merged dict; `main()` compiles and writes `compile_records(base_queries) +
  compile_records(addition_queries)` — i.e. output order is **structurally** base-prefix-then-
  additions, not an accidental consequence of dict insertion order.
- Assembly rule for additions is otherwise identical to their lane's base rule (same
  `CATEGORY_MAP` entry, same `DEFAULT_DATE_FROM`/`DEFAULT_DATE_TO`, same `START=0`,
  `DEFAULT_MAX_RESULTS=75`, same `sortBy=relevance`/`sortOrder=descending`) — none of the 3
  addition query_ids appear in `DATE_FROM_EXCEPTIONS` or `MAX_RESULTS_EXCEPTIONS`, so defaults
  apply untouched, matching the task's "增补查询装配规则与所挂 lane 相同" requirement.

## Static validation results (rerun at 51-query scope, all network-free)

| Check | Result | Details |
|---|---|---|
| `row_count_equals_51` (was `row_count_equals_48`) | PASS | got 51, expected 51 |
| `query_id_unique` | PASS | n_unique=51 |
| `no_placeholder_or_ellipsis_or_angle_bracket_residue` | PASS | clean |
| `no_stray_brackets_outside_submittedDate` | PASS | clean |
| `balanced_parens_and_quotes` | PASS | clean |
| `boolean_operators_fully_uppercase` | PASS | clean |
| `dates_well_formed_and_ordered` | PASS | clean |
| `each_lane_has_expected_query_count` (was `each_lane_has_exactly_6_queries` — now per-lane, since SF-L1/SF-L3 grew) | PASS | all lanes match `{SF-L1: 8, SF-L2: 6, SF-L3: 7, SF-L4: 6, SF-L5: 6, SF-L6: 6, SF-L7: 6, SF-L8: 6}` |
| `bonus_categories_match_frozen_mapping` | PASS | clean |
| `bonus_exceptions_applied_correctly` | PASS | clean |
| `bonus_record_sha256_recomputes_identically` | PASS | clean |
| `bonus_compiler_version_tiered_correctly` (new) | PASS | clean — all 48 base rows = `sfqc-1.0.0`, all 3 addition rows = `sfqc-1.1.0` |
| `bonus_output_order_is_base_prefix_then_additions_appended` (new) | PASS | clean — row order = `SF-L1-Q1..SF-L8-Q6` then `SF-L1-Q7, SF-L1-Q8, SF-L3-Q7` |

**OVERALL (in-script): PASS (0 failures / 13 checks, 8 required + 5 bonus)**

## Task-mandated additional checks (done at report-compilation time)

### ① 48-line byte-prefix invariance (old vs new)

Computed by reading `git show HEAD:wiki/survey/2026-07-15-sf-queries.jsonl` (the pre-A3-8, 48-line
canonical blob) and comparing it against the first 48 lines (i.e. bytes up to and including the
48th `\n`) of the freshly recompiled 51-line file:

| Artifact | sha256 |
|---|---|
| `git show HEAD:...sf-queries.jsonl` (48 lines, pre-A3-8 canonical) | `72674bfead4bdd29874f4318293637b047cc220c7fff65a157f990a7f5323e95` |
| First 48 lines of the new 51-line file (reconstructed with trailing `\n`) | `72674bfead4bdd29874f4318293637b047cc220c7fff65a157f990a7f5323e95` |

**Result: PASS — identical.** The `git HEAD` hash also matches the original report's cited jsonl
sha256 (`72674bfead4bdd29874f4318293637b047cc220c7fff65a157f990a7f5323e95`) verbatim, confirming
continuity: original-report artifact → git-committed blob → today's recompiled 48-line prefix are
all the same bytes. No base record was mutated by the A3-8 upgrade.

### ② Addition rows' `query_id` / `lane` / `compiler_version` fields

| query_id | lane | categories | compiler_version | record_sha256 |
|---|---|---|---|---|
| `SF-L1-Q7` | `SF-L1` | `cs.CL, cs.AI, cs.LG, cs.CV, cs.RO` | `sfqc-1.1.0` | `a6e2cd8baf11ea39de5d15a4253d822fb80473a671a27fa7dd127675aff294db` |
| `SF-L1-Q8` | `SF-L1` | `cs.CL, cs.AI, cs.LG, cs.CV, cs.RO` | `sfqc-1.1.0` | `7f9acbf51b32e0d08cf9c2c711529ba8188a730608b7b392dd5be8627c2b3432` |
| `SF-L3-Q7` | `SF-L3` | `cs.CL, cs.AI, cs.LG, cs.CV, cs.RO, cs.SD, eess.AS` | `sfqc-1.1.0` | `f52520dc089c3452f0fddb43c75d43280470b7d3535ac61e65614555773c4a72` |

All three: `date_from=202210010000`, `date_to=202607152359` (default window, no exception),
`start=0`, `max_results=75`, `sortBy=relevance`, `sortOrder=descending` — i.e. assembled with the
same rule as their lane's base queries, per spec. Spot-checked against unaffected base rows
`SF-L1-Q1` and `SF-L8-Q6`, both confirmed still `compiler_version = sfqc-1.0.0`.

**Result: PASS.**

### ③ Unregistered-`Q>=7` anti-mixing guard: exists and fires

The guard is `parse_all_queries()`'s per-lane comparison of parsed Q-numbers against
`expected_q_nums_for_lane(lane_id)` (base `1..6` plus whatever `ADDITIONS` registers for that
lane) — any parsed number outside that set raises `ParseError` (a `SystemExit` subclass), which
propagates to a nonzero process exit code. This was verified empirically (not just by code
reading) by loading the compiler module in-process and calling `parse_all_queries()` directly
against synthetic variants of the **real, current** protocol text with an injected unregistered
`- Q9` line — no file on disk was modified for this test; the injection happened purely on an
in-memory string:

| Scenario | Injection | Result |
|---|---|---|
| A | Unregistered `Q9` added to `SF-L2` (a lane with **zero** registered additions) | `ParseError` raised: *"SF-L2: expected Q-numbers [1..6] ..., found [1..6, 9]. UNREGISTERED Q-number(s) [9] ... refusing to silently absorb an unregistered addition."* |
| B | Unregistered `Q9` added to `SF-L1` (a lane that **already has** registered `Q7`/`Q8`) | `ParseError` raised: *"SF-L1: expected Q-numbers [1..6,7,8] (base [1..6] + registered ADDITIONS [7, 8]), found [1..6,7,8,9]. UNREGISTERED Q-number(s) [9] ..."* |
| C (control) | No injection — real, unmodified current protocol text | Parses clean: 48 base + 3 additions, `out_of_scope=['SF-L9']` — confirms the guard's presence does not produce any false positive on the actual document |

**Result: PASS** — the guard exists, fires on an unregistered addition regardless of whether its
lane already has other registered additions (B is the stricter case — it proves the check is keyed
to the *specific* registered Q-number set per lane, not merely "this lane is allowed some
additions"), and does not misfire on the real document (C).

## Compiled assembly spec applied (unchanged from original report, verbatim)

- Category expression: `SF-L1/L2/L4/L5` → 5-cat set; `SF-L3` → 5-cat + `cs.SD`/`eess.AS`;
  `SF-L6/L7/L8` → 3-cat set. The 3 A3-8 additions inherit their lane's set unchanged (`SF-L1-Q7`,
  `SF-L1-Q8` → 5-cat; `SF-L3-Q7` → 7-cat).
- Date window (double-closed): default `202210010000`–`202607152359` for all 3 additions (no
  exception applies to any addition query_id).
- Pagination: `start=0`, `max_results=75` for all 3 additions (no addition matches
  `MAX_RESULTS_EXCEPTIONS`, which remains scoped to `SF-L7-Q3` only).
- `sortBy=relevance`, `sortOrder=descending` — unchanged, all 51 rows.

## Attestation summary

- **联网检索查询执行数 (network search queries executed) = 0.** This compiler run and this
  report's verification steps performed zero HTTP calls, zero DNS lookups, zero sockets — pure
  local file read/parse/write plus in-process Python string manipulation for check ③'s synthetic
  injection test (never touched the network or any external service).
- Files modified by this task: exactly the 3 named in the task instructions —
  `scripts/survey/sf_query_compiler.py`, `wiki/survey/2026-07-15-sf-queries.jsonl`, and this report
  (`docs/checks/2026-07-16-sf-queries-static-validation-rerun.md`). No commit was made (working
  tree only, per instructions).
- Original report `docs/checks/2026-07-15-sf-queries-static-validation.md` left untouched — its
  content is now historical (documents the pre-A3-8, 48-query compile); this report is the current
  chain-of-custody reference going forward.

**OVERALL: PASS — 13/13 in-script checks + 3/3 task-mandated additional checks, 0 failures.**

---

## 敌意环后终态补记（2026-07-16,协调者亲验）

A3 批敌意环修复触及协议正文（§6 rl_identity 字段名对齐、frontmatter 环记录、§2 计数一处）,
均不在 §4 查询区。环后重跑 compiler：exit 0,13/13 静态检查 PASS,输出
`2026-07-15-sf-queries.jsonl` sha256 = `4e40658010d89833878e1f353a4975db5f86a52547f0fd10adbf093cf054a5e9`
（与本报告上文记录一致,逐字节不变）,48 行前缀与 git HEAD 版继续一致。**终态链条**：
协议（sha256 `d2518ec0d445ca394104d48185f21782d2af7f65382940e85e5cddbe779d6225`）→ compiler
（sfqc-1.0.0/1.1.0 分层）→ queries.jsonl（`4e406580…`,51 行）。上文所记 `db306898…` 为环中
快照,本节取代其链条职能（原文保留作 lineage）。联网检索查询执行数 = 0。
