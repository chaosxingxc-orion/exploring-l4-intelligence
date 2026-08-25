---
title: "Decision request: reconcile the Research-Objective required_truth token list with current truth"
date: 2026-08-25
role: "Engineering spec / decision request — prepares an owner decision, decides nothing"
scope: "wiki/Research-Objective.md and scripts/checks/test_ai_context_surface.py::test_research_objective_is_bounded_current_truth"
status: "OPEN — awaiting owner decision on six tokens"
changes_made_by_this_document: "none; neither the page nor the oracle token list is touched here"
---

# Decision request — the six failing `required_truth` tokens

## 1. Why this document exists

`scripts/checks/test_ai_context_surface.py::test_research_objective_is_bounded_current_truth`
carries a 43-token `required_truth` tuple that asserts, literally, that
`wiki/Research-Objective.md` still states each piece of current truth the program has decided
that page must state. Commit `fb04669` removed a calendar constant that sat **before** that loop
and aborted the method, so the loop went blind. With the constant gone the loop runs and six of
its 43 tokens fail.

`fb04669` deliberately did not repair them, on the grounds that the page has 3 bytes of headroom
against its 5,120-byte budget and that at least one token might be content the study has moved
past. This document supplies the per-token evidence so the owner can decide each one. **Nothing
in `wiki/Research-Objective.md` and nothing in the oracle's token tuple was changed to produce
this document.**

## 2. Blind window — verified, with one correction to the `fb04669` record

The aborting assertion was `self.assertEqual(date(2026, 8, 4), refresh_date)`, introduced at
`e9770b6` (2026-08-04) and removed at `fb04669` (2026-08-25).

| commit | date | page `last_refresh` | oracle pin | loop ran? |
|---|---|---|---|---|
| `a6edf40` | 2026-08-04 | 2026-08-04 | 2026-08-04 | **yes — last green run** |
| `047cf39` | 2026-08-05 | 2026-08-05 | 2026-08-04 | no |
| `28d6736` | 2026-08-05 | 2026-08-05 | 2026-08-04 | no |
| `26386cb` | 2026-08-07 | 2026-08-07 | 2026-08-04 | no |
| `c5cb168` | 2026-08-18 | 2026-08-18 | 2026-08-04 | no |
| `49c5414` | 2026-08-25 | 2026-08-25 | 2026-08-04 | no |
| `fb04669` | 2026-08-25 | 2026-08-25 | (constant removed) | yes |

**Correction to the `fb04669` commit message.** It states the contract "has not actually run
since 2026-08-07". The blind window in fact opens one commit earlier, at `047cf39` (2026-08-05),
which is the first commit whose `last_refresh` diverges from the pinned constant. The last green
run of the token loop is `a6edf40` (2026-08-04). The conclusion is unaffected: all three
token-dropping commits fall inside the window.

Attribution of every loss, from `git log -S <token> -- wiki/Research-Objective.md`, is confirmed:

- `26386cb` (2026-08-07) — 1 token
- `c5cb168` (2026-08-18) — 3 tokens
- `49c5414` (2026-08-25) — 2 tokens

## 3. Verdict table

Assertion site for all six: `scripts/checks/test_ai_context_surface.py:1814`,
`self.assertIn(token, text)`, inside the `for token in required_truth:` loop of
`AiContextRepositoryPolicyTests.test_research_objective_is_bounded_current_truth`. Tuple entries
are at the line numbers below.

| # | token (oracle line) | dropped by | classification | byte cost of the REPAIR option |
|---|---|---|---|---|
| A | `candidate method are Stage‑2 outputs` (1785) | `c5cb168` | **RETUNE THE TOKEN** | +103 (A and B share one sentence) |
| B | `final validation is Stage‑3` (1786) | `c5cb168` | **RETUNE THE TOKEN** | (included in A) |
| C | `SLUE-SQA-5, ContextASR-Bench and AMI` (1789) | `c5cb168` | **RETIRE THE TOKEN** | +77 |
| D | `H5 remains` (1791) | `49c5414` | **RETUNE THE TOKEN** | +2 |
| E | `External knowledge is introduced` (1799) | `26386cb` | **RETUNE THE TOKEN** | +15 |
| F | `wiki/archive/working/system-first-survey-current/` (1804) | `49c5414` | **REPAIR THE PAGE** | +71 (tight) / +92 (readable) |

Repairing all six costs **268 bytes** against **3 bytes** of headroom and **131 bytes** of
identified truth-neutral cuts (§5): a 134-byte shortfall. Restoring everything is not an option.
The recommended package — retune A/B/C/D/E, repair F — costs **71–92 bytes** and is fully funded.

## 4. Per-token evidence

### A + B — `candidate method are Stage‑2 outputs` / `final validation is Stage‑3`

**Dropped by** `c5cb168` (2026-08-18, "fit the 5KB budget + rebuild the context manifest").

Removed text, verbatim:

> Repository: `studies/speech-aware-evidence-acquisition/`; remote is private. Innovation and the
> candidate method are Stage‑2 outputs; final validation is Stage‑3 (paper repo).

Current page, verbatim (`## Formal, legacy and routing boundaries`):

> Carriers bind stages (Decision-Log continuation entry 91): Stage‑1 = umbrella; Stage‑2 =
> `studies/<slug>`, endpoint = qualified paper candidates; Stage‑3 = `papers/<slug>` under
> `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT`.

and, in `## Current gate and authority`:

> signed 2026-08-03; the single self-contained authority (GO + speech-only identity + Stage‑3 stop
> line) is

**Classification: RETUNE THE TOKEN.** The content survives in a stronger, operational form. "The
candidate method is a Stage-2 output" is exactly what "Stage‑2 = `studies/<slug>`, endpoint =
qualified paper candidates" says, and it names the carrier as well as the endpoint. The Stage-3
half is thinner on this page — it names the carrier, the gating contract token and a "Stage‑3 stop
line" rather than the phrase "final validation" — but the full claim is on the surface that loads
immediately **before** this page in the fixed reading order: `CLAUDE.md` / `AGENTS.md`
§ *Research boundary* states "final validation and publication-grade claims belong to Stage-3 in
the paper repo." The oracle already asserts guide content in
`test_agent_guides_and_contributing_route_without_copying_full_policy`, so the guarantee can be
re-homed without weakening it.

Recipe if accepted:

- replace `"candidate method are Stage‑2 outputs"` with `"endpoint = qualified paper candidates"`;
- replace `"final validation is Stage‑3"` with `"OWNER_GO_AND_PAPER_EXECUTION_CONTRACT"` (a token
  the page carries today and the tuple does not yet pin);
- add `self.assertIn("final validation and publication-grade claims belong to Stage-3", guide)`
  to the guide loop in `test_agent_guides_and_contributing_route_without_copying_full_policy`, so
  the phrase stays machine-pinned on the default surface where it actually lives.

If the owner prefers REPAIR instead, the cost is **+103 bytes** in context.

### C — `SLUE-SQA-5, ContextASR-Bench and AMI`

**Dropped by** `c5cb168` (2026-08-18).

Removed text, verbatim:

> SLUE-SQA-5, ContextASR-Bench and AMI are complete secondary speech carriers.

**The working hypothesis that this is content the research moved past is false.** Verified at
source:

- `wiki/Experiment-Assets.md:41` states the same fact today, verbatim in substance:
  > Current carrier readiness: Earnings21, Earnings22 and ConEC are materialized at pinned revisions
  > (`D0_CLOSED`); SLUE-SQA-5, ContextASR-Bench and AMI are complete speech-domain secondary carriers.
- `docs/datasets.lock.json` still declares the profile
  `"speech-aware-secondary": "SLUE-SQA-5, ContextASR-Bench, AMI and SlideASR-Bench public secondary
  speech carriers."`

**Classification: RETIRE THE TOKEN — but for a different reason than the one first proposed.**
The fact is true and live; what is wrong is the page it is pinned on. `wiki/Research-Objective.md`
delegates this class of fact twice in its own text — "route detail through
`wiki/Experiment-Assets.md`" and "`docs/datasets.lock.json` is the only live asset authority" — and
`wiki/Experiment-Assets.md` is the HOT page whose declared role is exactly the asset control plane.
Re-inserting the sentence would create a **second HOT carrier of the same current field**, which
`wiki/AI-Collaboration.md` §2 treats as a consolidation trigger and §1 forbids outright: "prose
cites the canon and never transcribes a parallel copy of the figures." That is the sense in which
re-inserting it makes the page less true as a governance object.

Recipe if accepted: delete the token from the Research-Objective tuple **and, in the same change**,
add a content assertion for `wiki/Experiment-Assets.md`. There is no content oracle for that file
today (only its manifest class and load policy, at test line 1887), so retiring the token without
the companion assertion loses the machine guarantee entirely. Suggested companion:

```python
assets = self.read_text("wiki/Experiment-Assets.md")
self.assertIn("SLUE-SQA-5, ContextASR-Bench and AMI", assets)
```

If the owner prefers REPAIR instead, the cost is **+77 bytes** in context.

### D — `H5 remains`

**Dropped by** `49c5414` (2026-08-25). Note that this commit's own message asserts "No status token
was dropped"; that claim is inaccurate — two tokens were dropped here (D and F).

Before, verbatim:

> historical evidence; H5 remains `WITHHOLD_NON_LOAD_BEARING`.

Current page, verbatim:

> claim in Stage‑2; the fixed Stage‑1B v5 320-work union stays historical evidence and H5 stays
> `WITHHOLD_NON_LOAD_BEARING`.

**Classification: RETUNE THE TOKEN.** The oracle pins the verb, not the fact. The fact is pinned
twice already and both pins are green:

- the sibling token `"WITHHOLD_NON_LOAD_BEARING"` (tuple line 1792) passes;
- `test_hot_state_preserves_stage1c_authority_boundary` asserts
  `H5[\s\S]{0,220}(?:pending|withhold|withheld|missing|not admitted)` and passes on "H5 stays
  `WITHHOLD_NON_LOAD_BEARING`".

Recipe if accepted: drop `"H5 remains"` from the tuple and replace it with a verb-agnostic binding
that is strictly stronger than the current pair, e.g.

```python
self.assertRegex(text, r"H5\s+\w+\s+`WITHHOLD_NON_LOAD_BEARING`")
```

If the owner prefers REPAIR instead, the cost is **+2 bytes** ("stays" -> "remains") and it fits
inside the existing 3-byte headroom with no cut at all. This is the cheapest of the six.

### E — `External knowledge is introduced`

**Dropped by** `26386cb` (2026-08-07) — the same commit that opened the blind window, so the
regression was invisible from the moment it was created.

Before, verbatim:

> External knowledge is introduced to
> address accessibility, current/proper-name and verifiability gaps, while controls must measure the new
> risks of irrelevant evidence, context pollution and reward hacking.

Current page, verbatim:

> External knowledge addresses
> accessibility, proper-name and verifiability gaps; controls must measure the new risks of irrelevant
> evidence, context pollution and reward hacking.

**Classification: RETUNE THE TOKEN.** Passive to active voice; the three gaps, the three risks and
the control obligation are all intact. The only substantive loss is "current/" from
"current/proper-name", which is a narrowing of the gap taxonomy, not of the claim the token pins.

Recipe if accepted: replace `"External knowledge is introduced"` with a voice-agnostic pin that
also captures the risk clause the sentence exists for, e.g.

```python
self.assertRegex(
    text, r"External knowledge [\s\S]{0,120}verifiability gaps[\s\S]{0,200}reward hacking"
)
```

If the owner prefers REPAIR instead, the cost is **+15 bytes** in context.

### F — `wiki/archive/working/system-first-survey-current/`

**Dropped by** `49c5414` (2026-08-25). The commit message records the drop as deliberate: "the
boundaries section loses only the cold archive pointer."

Before, verbatim:

> Literature work is a bounded delta lane
> through `wiki/survey/README.md`; the retired package is at
> `wiki/archive/working/system-first-survey-current/`. It reopens Stage‑1 only if new evidence
> invalidates the problem, carrier legality, information boundary or reproducibility contract.

Current page, verbatim:

> Literature work is a bounded delta lane
> through `wiki/survey/README.md`, reopening Stage‑1 only if new evidence invalidates the problem,
> carrier legality, information boundary or reproducibility contract.

**Classification: REPAIR THE PAGE.** The target is real and populated (40 tracked files under
`wiki/archive/working/system-first-survey-current/`), the fact is unchanged, and the removal was a
byte-budget casualty explicitly recorded as such. The RETIRE test — "re-inserting it would make the
current-truth page LESS true" — fails here: nothing about restoring it is untrue.

**Recorded dissent, so the owner can choose RETIRE with the argument in front of them.** The route
is not actually broken. `wiki/survey/README.md`, which the surviving sentence names in the same
breath, carries the row

> | Closed Stage‑1 survey package and superseded working material | `../archive/working/system-first-survey-current/` and sibling campaign dirs | Cold; load only for a named historical/replay question |

so the destination is one hop away through the router the page cites. `wiki/AI-Collaboration.md` §3
requires that "a current file must be self-contained and must never need the workbench or the
archive to be understood", and `CLAUDE.md` § *AI context routing* says never to broadly load
`wiki/archive/`. An archive path on the default-load page is therefore defensible but not
mandatory. If the owner takes this view, the recipe is to delete the token and add the
compensating assertion that `wiki/survey/README.md` carries the archive route, so the route stays
machine-guaranteed somewhere.

Concrete REPAIR wording (readable variant, **+92 bytes**):

```
`RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`. Literature work is a bounded delta lane
through `wiki/survey/README.md`; the retired Stage‑1 package is at
`wiki/archive/working/system-first-survey-current/`. Reopening Stage‑1 needs new evidence that
invalidates the problem, carrier legality, information boundary or reproducibility contract.
```

Tight variant, **+71 bytes**:

```
`RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`. Literature work is a bounded delta lane
through `wiki/survey/README.md` (retired package:
`wiki/archive/working/system-first-survey-current/`), reopening Stage‑1 only if new evidence
invalidates the problem, carrier legality, information boundary or reproducibility contract.
```

The path sits inside backticks, so the link scanner masks it as inline code; the pre-`49c5414` page
carried exactly this construction and `ai_context_surface_check` passed on it.

## 5. Paying for a repair — the budget and three truth-neutral cuts

`wiki/Research-Objective.md` is **5,117 bytes** of a **5,120-byte** budget (LF working tree, no CR
bytes; the Git blob is the same 5,117). Headroom: **3 bytes**.

Any REPAIR must free bytes first. Three candidate cuts, in decreasing confidence:

### Cut 1 — the `last_refresh` descriptive tail (frees 58 bytes) — recommended

```
-last_refresh: "2026-08-25 — SLURP baseline LOCKED; Audio2Tool G1 = mechanics only"
+last_refresh: "2026-08-25"
```

Why no current truth is lost: the oracle reads only `^last_refresh: "(\d{4}-\d{2}-\d{2})` (see
`HOT_REFRESH_DECLARATIONS`, added by `fb04669`), so the tail is free-form prose with no machine
consumer. Its two claims are restated verbatim in substance in `## Next action` eleven lines below
— "**The SLURP baseline is LOCKED**" and "**Second carrier Audio2Tool G1 — MECHANICS AND FIRST
SIGNAL ONLY, no generality claim**". This deletes a duplicate summary, not a fact. The paired-page
equality check against `wiki/Per-Work-Status.md` compares dates only and is unaffected.

### Cut 2 — the study-repo config path (frees 55 bytes)

```
-retain-override was falsified out of sample and removed; locked cell
-`configs/policy/kb-policy-v1-dev100.json`. **Second carrier
+retain-override was falsified out of sample and removed. **Second carrier
```

Why no current truth is lost: the page's own reading-order note states "the study repo owns
code/config/tests", so naming a study config file here contradicts the delegation the page itself
declares one screen earlier. The locked cell is canonical in the study repo's
`docs/readiness/2026-08-25-baseline-lock-verdict.md` and in
`wiki/experiments/speech-aware-evidence-acquisition/README.md`, which the same paragraph already
cites as its digest. Residual risk: a reader loses the one-hop identity of the locked cell and must
follow the digest pointer — acceptable, since that pointer is in the same sentence.

### Cut 3 — the dispatch count (frees 18 bytes)

```
-identity-preserving on the locked cell, and the post-repair arm fires the supply path (15 of 104
-dispatch, gains method-attributable) with a population delta **NOT separated from zero**.
+identity-preserving on the locked cell, and the post-repair arm fires the supply path with gains
+method-attributable and a population delta **NOT separated from zero**.
```

Why no current truth is lost: `15 of 104` is a figure canonical in the fifth-arc section of the
experiment digest. Both load-bearing qualifications — "gains method-attributable" and "**NOT
separated from zero**" — are preserved verbatim. This is the weakest of the three cuts; it removes
a concrete number rather than a duplicated one, and should be taken only if Cuts 1 and 2 do not
cover the chosen package.

### Funding table

| package | cost | funded by |
|---|---|---|
| **Recommended**: retune A/B/C/D/E, repair F (tight) | 71 | Cut 1 + Cut 2 + 3 headroom = 116 |
| Recommended, readable F wording | 92 | Cut 1 + Cut 2 + 3 headroom = 116 |
| Add REPAIR of D ("stays" -> "remains") | +2 | 3-byte headroom alone |
| Add REPAIR of E | +15 | Cut 3 |
| Add REPAIR of A+B | +103 | not funded by Cuts 1–3 |
| Repair all six | 268 | **not fundable** — 134-byte shortfall |

Cut 1 alone (58 + 3 = 61) does not cover even the tight F wording; Cut 1 + Cut 2 is the minimum
viable funding for the recommended package.

## 6. What is being asked

One decision per row of §3, plus, for every RETIRE or RETUNE, approval of the companion assertion
so no guarantee is silently dropped. The paired change must land in one commit:
`wiki/Research-Objective.md` + `scripts/checks/test_ai_context_surface.py` +
`python scripts/checks/build_ai_context_manifest.py` (the page's `sha256` in
`docs/integrity/ai-context-manifest.json` is currently
`203b2d86d5c2ad8ae3d3f0cd0b18e4397276c2405e2584ce8d4879b1e586102c` and must be re-rendered).

## Appendix A — the stale endpoint token (reported, not acted on)

`wiki/Research-Objective.md:16` carries

```
DIRECTION_LOCAL_PIPELINE__R1_SUNSET__SPEECH_AWARE_EVIDENCE_ACQUISITION_OWNER_GO__STAGE2A_R0_INCOMPLETE__R1_WITHHELD
```

**Both trailing fields are stale**, not only the one flagged.

`STAGE2A_R0_INCOMPLETE` entered at `26386cb` (2026-08-07) from the independent rereview, which
decomposed R0 into R0.1 (model-free readiness memo + innovation ledger), R0.2 (model-free
engineering baseline) and R0.3 (the real smoke `SAEA-E-001`), and ruled `R0.1 = NOT_DONE`,
`R0.3 = NOT_AUTHORIZED_NOT_RUN`, `R0 overall = INCOMPLETE`
(`wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-rereview-2026-08-07/`). Since
then:

- **R0.2** — the operator-path repair was merged in that same commit.
- **R0.1** — closed. Its survey product is
  `wiki/experiments/speech-aware-evidence-acquisition/published-baselines.md`, whose front matter
  reads `source_surveys: "study repo docs/readiness/2026-08-07-*.md (R0.1, model-free)"`, and which
  contains zero remaining `(fill)` placeholders.
- **R0.3** — closed. `SAEA-E-001` ran on 2026-08-09 and is registered in the experiment ledger; its
  decision column reads "R0 exit criterion (measurement integrity) MET".

`R1_WITHHELD` entered at `28d6736` (2026-08-05), when the independent review returned REPAIR, and
denotes the study's first post-R0 experiment round, not the sunset direction R1 (that is the
separate leading `R1_SUNSET` field). It was released by
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-08-owner-go-baseline-reproduction.md`,
which adopts the R1 re-plan `docs/readiness/2026-08-07-r1-replan-reproduction-plan.md` (P0–P4) as
the execution form and sets the execution sequence beginning with `SAEA-E-001`. Everything from the
second arc through the fifth arc of the experiment digest is that program executing.

**Paired-change recipe (owner decision required — this is the program endpoint token).** The exact
string has three carriers:

1. `wiki/Research-Objective.md:16` — the live claim.
2. `scripts/checks/test_ai_context_surface.py:1782` — `required_truth` tuple entry.
3. `wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-rereview-2026-08-07/2026-08-07-implementation-response.md`
   — an **immutable audit record**. It is never rewritten; it correctly states what was true on
   2026-08-07.

Land 1 and 2 in one commit (splitting them leaves a red gate at HEAD), then re-run
`python scripts/checks/build_ai_context_manifest.py` because the page hash moves, then re-run the
suite. A successor field pair should be shorter than the current one, so the change frees budget
rather than consuming it. Choosing the successor value is an owner call, not an implementer's:
the token is the program's stage-accounting endpoint and the study's own current stage language is
"Stage-2A discovery in flight (standing GO)" with Stage-2B qualification not yet claimed.

## Appendix B — the Chinese owner-authority records (reported, not acted on)

`wiki/experiments/speech-aware-evidence-acquisition/2026-08-06-owner-budget-caps-retirement-contract.md`
is 2,992 bytes with 554 CJK ideographs (32.1% of its characters). Its YAML front matter is English
(`title`, `record_id`, `status: "SIGNED_BY_OWNER"`); the body — the disposition, the owner's stated
reason, and the list of mechanisms explicitly **not** retired — is Chinese.

**It is not alone.** A full scan of that directory:

| file | CJK chars | share |
|---|---|---|
| `2026-08-04-owner-speech-domain-scope-and-identity-contract.md` | 1,848 | 29.5% |
| `2026-08-03-owner-go-and-execution-contract.md` | 848 | 19.8% |
| `2026-08-06-owner-budget-caps-retirement-contract.md` | 554 | 32.1% |
| `2026-08-08-owner-go-baseline-reproduction.md` | 403 | 25.6% |
| `2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md` | 256 | 15.9% |
| `2026-08-15-owner-go-dual-track-agentic.md` | 8 | 0.4% |
| `2026-08-04-owner-consolidated-execution-contract.md` | 0 | — |

**Why no gate catches this.** `validate_english_only` in `scripts/checks/ai_context_surface_check.py`
fails closed on any CJK codepoint, but only over the explicit `ENGLISH_ONLY_PATHS` allowlist (25
entries: root Markdown, the sixteen HOT wiki pages, `wiki/survey/README.md`, `papers/README.md`,
`studies/README.md`, `docs/architecture.md`). `wiki/experiments/**` is not in the set. The
function's own docstring says the scope is "never 'every HOT file'" precisely so the rule cannot
silently expand onto immutable records — so this is a deliberate boundary with an uncovered gap
behind it, not a checker defect.

**Why a drive-by rewrite is the wrong move.**

1. These are signed owner authority records. `2026-08-06` carries `status: "SIGNED_BY_OWNER"`, and
   `2026-08-08` and `2026-08-15` quote the owner's directive verbatim in the YAML `authority`
   field. Restating an owner's signed words in another language changes the text that authority
   rests on; that is the owner's call.
2. The `2026-08-06` record is load-bearing today. The study's `CLAUDE.md` cites it as the authority
   that retired the numeric budget caps while keeping exposure pre-registration and one-shot
   attempt semantics in force, and
   `wiki/audit/speech-aware-evidence-acquisition-r0-review/INDEX.md` cites it by path as "Owner
   action arising from this campaign, filed as execution authority (not an audit artifact)", with
   the reviewer-facing consequence that "absence of numeric-cap enforcement is an owner scope
   reduction, not a defect".
3. **The program already has a protocol for exactly this, and it is not an in-place edit.** At
   `c6053a2` (2026-08-16) the consolidated execution contract was **re-issued** in English: terms
   unchanged, pre-translation bytes preserved as a named Git blob
   (`8ddd0cf2a96908befc8b49e69602185729ba17ba`), `studies/registry.json:decision_record_blob`
   re-pinned to the new blob (`d1d8fce657ec593e35ff140ebab13f6d3545e5c6`) in the same commit with
   the two agreeing, and `wiki/Decision-Log-2026-08.md` given continuation entry 94 by append only.
   The commit message states the standard plainly: "this is a language conversion, not an edit."

**What a faithful repair would involve**, if the owner sanctions it:

- re-issue each record in English with terms unchanged, preserving each pre-translation blob id in
  the commit message;
- keep every verbatim owner directive in its original characters as a quoted source with an English
  gloss beside it — the pattern `2026-08-15-owner-go-dual-track-agentic.md` already uses (English
  body, the owner's answers kept verbatim and glossed);
- check for and re-pin any blob reference. `studies/registry.json` pins only
  `2026-08-04-owner-consolidated-execution-contract.md`, which is already English, so on current
  evidence no registry re-pin is needed — but this must be re-verified at the time of the change;
- append `wiki/Decision-Log-2026-08.md` continuation entry 95 (94 is the current highest);
- decide separately whether `ENGLISH_ONLY_PATHS` should be extended to
  `wiki/experiments/**/*.md`, so the rule stops depending on someone noticing. That extension would
  turn a prose principle into an executable one, per first principle #3, and is the durable fix.

Nothing above was executed. No file in `wiki/experiments/` was translated, edited, or moved by this
document.
