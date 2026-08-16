---
title: "SAEA: adversarial verdict on the 2026-08-16 continuation proposal and the corrected forward plan"
date: "2026-08-16"
status: "OWNER_RULINGS_RECORDED_2026-08-16__SEE_SECTION_6"
reviewed_document: "docs/superpowers/specs/2026-08-16-speech-aware-evidence-acquisition-continuation-extension-and-correction-proposal.md"
review_method: "two independent Opus analysts (adversarial claim audit + operational reconstruction), Fable synthesis"
execution_contract: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md"
live_constraint: "P2 resume block in flight at authoring time; study tree frozen at 7bf251f until terminal"
---

# SAEA: Proposal Verdict and Corrected Forward Plan

## 1. Verdict on the GPT-5.6 continuation proposal

**Adopt roughly one third, correct the spine, reject three parts.** The proposal's empirical
section survived a full audit (all eleven checkable numbers verified against committed bytes; it is
more current than `wiki/Research-Objective.md`, which still quotes the superseded 3-call pilot).
Its instrumentation-and-discipline layer is genuinely valuable. Its sequencing, scale, claim-tier
handling, survey table, and reward design do not survive adversarial review.

### Adopt essentially as written

- **§1.5 speech-mediated admission test (G1–G6)** — the repo has no written scope gate and four
  carriers landed within ten days; add an owner-admission override clause (the test as written
  would disqualify SLURP, which the owner admitted 2026-08-15).
- **§1.6 preserve/replace layer table** — resolves the "build on the existing solution" ambiguity;
  algorithms have no protected status, the scientific contract and measurement substrate do.
- **§5.4 causal decomposition + ticket E3 (opportunity ledger)** — confirmed absent from code;
  converts a null result into an assignable stage. Highest-value engineering item together with:
- **Ticket E1 (evidence-packet legality fields)** — `span_source` / `reference_source` /
  `legality_tier` / `source_tier` exist today only as prose in an arms-file header; the study's
  most important control ("either field gold-derived → whole arm ceiling-tier") is enforced by a
  human comment. Make it machine-enforced, fail-closed.
- **§8.2 unit-of-analysis rule and §9.4 reliability rules**; **§12 milestones**; **§13
  stop/narrow/promote rules**; **§10.1/10.2 model anchoring** (no model change while P2,
  routing, construction, or adapters are open).

### Adopt with corrections

- **WP0 (close P2)** — rewrite around the facts: every P2 arm is ceiling-tier, the HER clause of
  the AFFIRM rule is already guard-bound on r0bias (3 accepted splices < 10), and effective paired
  n is 6. UNRESOLVED is the modal outcome; an AFFIRM licenses operator-vs-operator ordering under
  oracle references only, and can never promote C3 without a legal-tier successor arm.
- **Sequencing** — the proposal runs construction (WP1) before routing (WP2); the registered
  rectification plan (2026-08-15) orders the oracle-flag-routing recall gate FIRST, so wasted
  construction cannot recur. Keep the registered order.
- **Scale** — the proposal's ladders total >50 result-bearing cells (>400 GPU-hours on one 5090)
  while the headline weakness is p=.19 at n=10 and a frozen 44-call discovery split sits unused.
  Spend the next block's compute on **n**, not cells; a power analysis precedes any new block.
- **Ticket E0 (flight protection)** — redesign around the actual defect class. The clean-tree
  preflight it specifies already exists and already passed on the run that died; the block was
  killed by a *mid-flight* working-tree mutation from a concurrent writer. Correct fix: a flight
  lockfile honored by all sessions/agents, plus narrowing the manifest bind from whole-tree
  porcelain to HEAD + a content hash of the load-bearing surface (`src/`, `configs/`,
  `docs/arms/`).
- **WP4B (SlideASR-Bench transfer)** — the asset is registered but has no contract §4 role
  amendment and no owner carrier admission; blocked until both exist.
- **WP5 (baselines)** — keep the contract-mandated `INCONCLUSIVE_BASELINE_NOT_READY` fail-closed
  token; self-implemented "behavioral arms" of code-less priors are never load-bearing baselines.

### Reject

- **§5.3 reward vector** — three of nine components are gold-referenced; using them for online
  action selection puts gold in the runtime path, which `contracts/boundary.py` refuses
  mechanically and the proposal's own §1.3 forbids. Delete, or rewrite as an explicitly offline
  evaluation vector with a "never an online action input" clause.
- **§11 survey table as written** — two citations not locally attested (one with a
  fabrication-shaped URL), three with venue/title drift, 13 of 14 without receipts, three named
  artifacts unregistered. Rebuild through the survey registry with receipts before any citation is
  reused.
- **§10.3 R0–R3 baseline-class naming** (collides with three existing meanings of R0/R1/R2 in
  this program) and **§15 org chart** (roles that do not exist here; keep only its parallelism
  rule: nothing may touch a live arm's bytes, thresholds, prompts, metrics, or interpretation).

## 2. Operational state at authoring (2026-08-16 ~12:30 EDT)

- P2 resume block detached-launched 06:58 after the 00:21Z dirty-tree abort. **r1verify DONE**
  (COMPLETED, bound to `7bf251f`, 2h17m), **r2draft DONE** (COMPLETED, 2h35m), **r0wrong RUNNING**
  (3/10 derivations at 12:23), **r1wrong QUEUED**. Block terminal ≈ 16:00 local ± 40 min.
- r0bias is sealed salvage, and — correction to both the proposal and the study repo's own prose —
  **its one-shot read has already been spent** (offline salvage before HER/RIR pinning; disclosed
  in the umbrella amendment). The study repo still says "UNREAD"; that is a documentation defect.
- The salvage read currently survives only as prose plus scripts in an ephemeral session
  scratchpad (`95b8e5b0-…`); no durable scores artifact exists. Archival is the first gap task.
- Known amber items: umbrella `ai_context_surface_check` red on the amendment file's location;
  I2 freeze-scope ambiguity (six umbrella commits landed during r1verify's flight; study tree
  stayed clean, no harm); GPU SW-power-cap oscillation (throughput currently normal); one 13-min
  r1verify attempt has no terminal manifest at all (ledger reconciliation note needed).

## 3. Forward plan

Delegation model (standing): **Fable** plans, preregisters, reviews, writes verdicts. **Opus**
babysits flights, executes registered reads, does analysis/archival/survey verification. **Sonnet**
implements engineering tickets in GPU gaps only, TDD, no installs (PYTHONPATH armor), one ticket
per brief. No code agents while any campaign flies.

### Phase 0 — now → block terminal (~16:00)

Study tree frozen at `7bf251f`. A read-only watcher polls for r1wrong's terminal manifest and for
stalls (>35 min without file activity). No intervention on the GPU unless derivation cadence
exceeds ~25 min/file; the live fix (`nvidia-smi -lgc 1200,2500`) is a decision, not a reflex.

### Phase 1 — GPU gap tasks (ordered; G2+G4 are the critical path to reads)

| # | Task | Owner |
|---|---|---|
| G1 | Preserve the r0bias salvage: inventory the `95b8e5b0` scratchpad, copy scripts/outputs into a durable hash-addressed study location; if no output bytes survive, reproduce them by deterministic archival replay of the *already-spent* read from the sealed trace, labeled as such — never a second read. | Opus |
| G2 | Mirror the HER/RIR amendment into study `docs/` (obligation in the amendment's §6). | Sonnet |
| G3 | Supersede the stale "UNREAD / will be read" prose (exposure ledger `:264`, resume arms `:31-35`) with dated append-only correction notes; add the missing-manifest reconciliation note for attempt `…T025734Z-23a43f`. | Sonnet |
| G4 | Implement the HER/RIR + pre-registered read suite as pinned, tested offline scoring scripts (formulas verbatim from the amendment, degenerate-denominator guards included; `PYTHONDONTWRITEBYTECODE=1`). | Sonnet |
| G5 | Diagnose and repair the red `ai_context_surface_check` (`new-audit-artifact-outside-audit-root`) as a paired policy+oracle change if the placement is correct, or a file move if not. | Sonnet |
| G6 | Owner ruling on I2 scope: proposed — study-repo freeze is hard; umbrella edits allowed during flight; umbrella commits touching the study's governance surface wait for gaps. | Owner |

### Phase 2 — P2 closure (after G2+G4 land and are reviewed)

Execute the pre-registered reads mechanically (Opus runs, Fable reviews and writes the verdict):
co-primary paired Wilcoxon on macro and entity-WER (8284-token ledger, effective n=6), HER and RIR
under the <10 guards, wrong-reference copy count on pre-localize replay text, format-normalized
secondary, per-term flips. **Check the voiding condition first** (wrong-reference copying in R1/R2
voids the audio-verification claim regardless of WER deltas), then the AFFIRM limbs. Expect the
HER limb UNRESOLVED. The exit artifact separates scientific outcome, vehicle reliability, late
metric pinning, and required clean confirmation — and states the ceiling-tier limit explicitly.
Flip `consumed` and append verdicts to the exposure ledger. Update `wiki/Research-Objective.md`
(currently stale) in place.

### Phase 3 — next experimental blocks (registration only after Phase 2)

1. **N0 — power analysis** (Opus, model-free): from the N10 block's paired effect sizes, size the
   next block against the frozen 44-call discovery split; report n for 80% power on both ledgers.
2. **N1 — routing gate first** (per the registered rectification order): measure how much of
   oracle routing the roster-band flag retains — as far as possible model-free from existing
   immutable traces (this is what ticket E3' enables); register a minimal live block only if the
   traces cannot answer it.
3. **N2 — legal-tier successor block**, content branch-dependent:
   - **AFFIRM** → R1-verify framing with *legal* references (metadata roster / lexicon v2) at the
     N0-sized n; this is the only path that can ever promote C3.
   - **COLLAPSE** → drop operator language per the registered rule; next block is legal targeted
     small-N supply vs. global metadata roster at the N0-sized n.
   - **UNRESOLVED** → decide by the live limbs (R2−R1, copy-rate); default to the legal-tier
     R1-verify block with the claim narrowed to what resolved.
4. **Deferred behind their gates**: WP1 construction ladder (post-routing-gate; at most 2 variants
   vs. metadata, budgeted); task ladder with SLURP first (admission receipts required); Audio2Tool
   stays probe-scoped; SlideASR-Bench blocked on owner admission.
5. **Parallel model-free lanes**: survey repair with receipts (Opus); Sonnet engineering backlog
   in gaps — E1' legality fields, E3' opportunity ledger, E0' flight lockfile + narrowed manifest
   bind, each TDD with the full suite green (baseline 1752 passed / 9 skipped).

## 4. Owner decisions — expanded analysis

### D1 — ratify the verdict on the proposal set

The proposal is self-declared `DRAFT_FOR_OWNER_REVIEW__NO_NEW_EXECUTION_AUTHORITY`; nothing in it
has force until ratified. Scope note: the 2026-08-16 draft batch contains five documents; this
verdict covers the SAEA continuation proposal and its two SAEA companions. The two
other-direction specs (agentic full-duplex; interleaved perception–reasoning–revision) are
umbrella Stage-1 candidate material and are **not** part of this decision.

- **Option A — ratify as delivered (recommended).** The adopted items create engineering work but
  no execution authority; the corrections restate already-registered positions (routing-first
  order, legality doctrine, ceiling-tier rule); the rejections are each grounded in a machine
  check or a receipts audit. Consequence: Sonnet backlog becomes definable; §11 citations are
  quarantined until the survey lane re-verifies them.
- **Option B — ratify with owner modifications.** Legitimate, e.g. softening the §11 rejection to
  "quarantine pending receipts" (functionally identical) or overriding the SLURP carve-out.
- **Option C — reject wholesale.** Loses E1/E3/§1.5, which fill gaps nothing else in the repo
  fills; not recommended.
- **Option D — defer until the P2 verdict.** Costs little for WP1+ content but leaves the
  engineering backlog undefined during the very GPU gaps where Sonnet could build it.

### D2 — I2 freeze-scope ruling

The registered I2 text says "no commits of any kind during any arm flight" and the ledger says it
"governs the whole block"; six umbrella commits nevertheless landed inside r1verify's flight with
no mechanical harm (the manifest bind reads only the study repo). The actual kill last night was a
mid-flight *study-tree* edit. One nuance: the HER/RIR amendment also landed mid-flight and touches
the live block's *semantics* — harmless only because it was pinned before any affected read and
disclosed.

- **Option A — program-wide literal freeze.** Safest, but sterilizes 2–12h windows for work that
  cannot touch the flight (translations, survey, umbrella governance), and is already contradicted
  by accepted practice.
- **Option B (recommended) — split ruling.** (i) Study repo: hard freeze — no edits, commits,
  checkouts, or installs by any session or agent from launch to terminal manifest. (ii) Umbrella:
  mechanically free (not on the runtime path). (iii) Exception class: umbrella changes that alter
  a live block's registered semantics (branch rules, metric definitions, arms interpretation) must
  wait for the gap, or — if urgent — land only before any affected read, with explicit disclosure,
  exactly as the HER/RIR amendment did. Ticket E0' later makes (i) machine-enforced.
- **Option C — leave ambiguous.** Guarantees a repeat with multiple parallel sessions active.

### D3 — SlideASR-Bench admission

Registered asset (MIT, test split only, `speech-aware-secondary`) but no contract §4 role
amendment and no owner carrier admission. Nothing upstream waits on it: WP4B sits behind the M2/M3
gates regardless.

- **Option A (recommended) — confirm blocked; revisit at the M3→M4 transition** with a G1–G6
  admission receipt plus a human/synthetic provenance audit as the entry evidence.
- **Option B — admit now.** Buys nothing usable and invites the benchmark-tour failure mode the
  proposal itself prosecutes.
- **Option C — reject permanently.** Premature; the provenance audit has not run.

### D4 — n-over-cells compute policy

Rough sizing from the recorded evidence: the metadata-vs-zero paired result (p=.19, n=10) implies
an effect size d≈0.41; 80% power at α=.05 needs n≈46–48 — the frozen 44-call discovery split is
almost exactly that size (power ≈0.77–0.78 at n=44). Observed wall cost is ~2.3–2.6h per 10-call
arm, so a 44-call arm ≈10–12h and a 2–3-arm paired block ≈20–36h of continuous flight.

- **Option A (recommended) — one-shot fixed n=44 block**, preconditioned on ticket E0' (a 1–1.5
  day flight without a lockfile is an unacceptable repeat risk) and on N0 (a proper power analysis
  from the real per-call paired diffs before registration; the d≈0.41 estimate is itself noisy at
  n=10).
- **Option B — staged/interim looks.** Rejected: interim reads collide with the read discipline
  and demand pre-registered alpha spending for no benefit at this scale.
- **Option C — n=22 subset.** Halves cost but yields ≈50% power at the observed effect: a coin
  flip that would likely reproduce the p=.19 stalemate.
- **Option D — keep n=10, buy cells (the proposal's implicit stance).** Rejected by the review.

### D5 — r0bias archival semantics (conditional)

The registered rule reads "read EXACTLY ONCE from that attempt". Preservation plan: first
inventory the `95b8e5b0` scratchpad and copy scripts *and any existing output bytes* into a
durable, hashed study location (no re-computation — plainly legal). Only if no output bytes
survive does a decision arise: authorize a deterministic archival re-computation from the sealed
trace, labeled as archival replay of the already-spent read (no model contact, same pinned
scripts) — or accept a prose-only record and log it as a limitation. Recommendation if it comes to
that: authorize the labeled archival replay; an auditable number beats an unauditable sentence.

## 5. Expanded task plan

### Phase 0 — in force now (block terminal ≈16:00±40min)

| ID | Task | Owner | Status |
|---|---|---|---|
| P0.1 | Read-only block watcher (terminal manifest / >35min stall), 10-min polls | Fable (running) | active |
| P0.2 | On wake only: GPU cadence check; intervention (`nvidia-smi -lgc`) is owner-decision, not reflex | Fable | armed |
| P0.3 | Sonnet briefs finalized so the gap starts instantly | Fable | done (this doc) |

### Phase 1 — GPU gap (est. 2–4h wall; G0 first, G4 = critical path)

| ID | Task | Owner | Precondition | Acceptance |
|---|---|---|---|---|
| G0 | Verify all four arms terminal; reconcile meters vs registered cells; confirm tree clean at `7bf251f`; check for parallel-session commits | Opus | terminal manifest | reconciliation note drafted |
| G1 | Salvage preservation: inventory `95b8e5b0` scratchpad; copy scripts+outputs to a hashed study location; if outputs absent → STOP, escalate D5 | Opus | G0 | SHA-256 manifest; no re-computation without D5 |
| G2 | Mirror HER/RIR amendment into study `docs/` (verbatim, provenance header: umbrella `34fb703`) | Sonnet | G0 | header-only diff vs source; committed via `git commit -F` |
| G3 | Append-only corrections: supersede "UNREAD/will be read" prose (ledger `:264`, resume arms `:31-35` — dated appendix, never rewrite registration bytes); reconcile the manifest-less attempt `…T025734Z-23a43f` | Sonnet | G0 | appends only; committed |
| G4 | Pinned offline read suite: paired Wilcoxon macro+entity (effective n=6; four zero-candidate calls excluded per registration), HER/RIR verbatim per amendment incl. <10 guards → raw counts → UNRESOLVED, wrongref copy count on PRE-localize text, format-normalized secondary, per-term flips. TDD with synthetic fixtures; **must not open real P2 results during development**; `PYTHONDONTWRITEBYTECODE=1` | Sonnet | G2 | suite ≥1752 green; fixtures reproduce exact numerators/denominators; Fable review before real data |
| G5 | Diagnose red `ai_context_surface_check` (`new-audit-artifact-outside-audit-root`); implement only check-side repair; a file-move needs Fable review (references exist) | Sonnet | — | gate green or reviewed move proposal |
| G6 | I2 ruling per D2 | Owner | — | ruling recorded |
| G7 | Commit this document to the umbrella after D1 | Fable | D1 | committed |

### Phase 2 — P2 closure (after G2+G4 review; est. 1–2h)

| ID | Task | Owner |
|---|---|---|
| R1 | Run the pinned read suite over the four COMPLETED arms + preserved r0bias record; raw tables only, no interpretation | Opus |
| R2 | Apply branch rules mechanically — voiding condition first (wrongref copying in R1/R2), then AFFIRM limbs (R2−R1>0; R1 vs R0-bias at matched entity gain with lower HER — expect guard-bound; copy-rate materially lower under verify), then COLLAPSE test. Write the WP0 exit artifact (scientific outcome / vehicle reliability / late pinning / required clean confirmation) with the ceiling-tier limit stated | Fable |
| R3 | Flip `consumed`, append verdict rows; refresh `wiki/Research-Objective.md` in place | Sonnet (Fable review) |
| R4 | Owner briefing: verdict + which N2 branch fires | Fable |

### Phase 3 — next blocks (from tomorrow)

| ID | Task | Owner | Gate |
|---|---|---|---|
| N0 | Power analysis from real per-call paired diffs (macro + entity); n for 80%/90% power; validates the d≈0.41 estimate | Opus | model-free |
| N1 | Routing gate from existing immutable traces: oracle-reachable errors selected by roster-band flag (recall), false-selection burden; live block only if traces cannot answer | Opus (+Sonnet for E3' if needed) | registered routing-first order |
| N2 | Legal-tier successor block at N0-sized n: AFFIRM → legal-reference R1-verify; COLLAPSE → legal targeted supply vs metadata roster; UNRESOLVED → legal R1-verify with narrowed claim | Fable registers; Opus babysits | P2 verdict + E0' + N0 |
| E0' | Flight lockfile honored by all sessions/agents + manifest bind narrowed to HEAD + content hash of `src/`, `configs/`, `docs/arms/` (measurement-substrate change: own registration, migration tests, legacy manifests stay readable) | Sonnet | gap only; before N2 |
| E1' | Machine-enforced packet legality fields (`span_source`/`reference_source`/`legality_tier`/`source_tier`), fail-closed either-field rule | Sonnet | gap only |
| E3' | Opportunity ledger generalizing G4: coverage→route→delivery→verify→accept denominators from immutable events | Sonnet | gap only |
| S1 | Survey repair: hard-verify the two unattested citations; rebuild §11 rows with receipts; classify priors per contract §4 with `INCONCLUSIVE_BASELINE_NOT_READY` | Opus | model-free, anytime |

## 6. Owner rulings (recorded 2026-08-16, conversational instruction)

- **D1 — ratified**, with the §11 survey quarantine resolved actively: an Opus web-verification
  pass over all 14 cited works (plus the three named artifacts) launched immediately; fetch log
  under `wiki/survey/workbench/2026-08-16-proposal-citation-verification/`. Worth-citing verdicts
  will replace the §11 rows.
- **D2 — Option B ratified.** Study repo: hard freeze during any arm flight (no edits, commits,
  checkouts, installs by any session or agent). Umbrella: mechanically free. Changes touching a
  live block's registered semantics wait for the gap, or land only before any affected read with
  explicit disclosure. E0' will machine-enforce the study freeze.
- **D3 — owner guidance:** locally registered/downloaded assets carry a prior positive assessment
  (referenced by other papers or previously judged worth referencing); use them as needed. Applied
  reading: SlideASR-Bench needs no fresh owner round-trip at first use — the formal contract §4
  role amendment is pre-authorized in principle and is executed when WP4B actually starts (still
  behind the M2/M3 gates).
- **D4 — approved with the owner's process mandate:** before the n=44 experiment flies, run the
  dataset preprocessing for the 34 unflown calls at full CPU concurrency (~20 workers, RAM-capped,
  throughput numbers as a manifest deliverable). Confirmed: preprocessing loads no omni model —
  the frozen core loads only when arms fly. Timing: preprocessing starts at the P2 GPU gap, not
  during the live flight, because (i) mixed heavy-CPU + GPU-decode load is the documented trigger
  for the 232 MHz SW-power-cap lockup and the GPU is already oscillating, and (ii) the tool
  campaign's exposure-ledger registration is a study-repo edit, which the D2 freeze forbids until
  terminal. New task **PRE** inserted into Phase 1 (below).
- **D5 — pre-authorized:** if salvage preservation (G1) finds no output bytes, the deterministic
  archival replay of the already-spent r0bias read (same pinned scripts, sealed trace, zero model
  contact, labeled as archival replay) may proceed without a further owner round-trip.

**PRE — dataset preprocessing for the 44-call block (inserted after G0):**
register the tool-campaign exposure row first (study commit, in the gap), then launch the
preprocessing of the 34 unflown earnings21 discovery calls at ~20 workers: slice derivation
(90s-era buffers), per-call metadata rosters, entity/benchmark ledger construction (gold stays on
the scoring side only, never in runtime artifacts), and any MMS_FA alignment the lexicon lane
needs. Owner-mandated deliverables: per-file hashes, aligned/failed counts, throughput
(slices/min + wall). Runs in background across Phases 1–2; must be COMPLETE and hash-manifested
before N2 registration. Owner: Opus supervises, CPU-only, no omni model load.

### Contingencies

- **Watcher exits STALL:** diagnose processes + GPU clocks first (`clocks.sm` first — known SW-power-cap
  failure); a chain death is re-launchable for un-completed attempts under the same registration
  (one-shot semantics govern *reads*, and re-flying aborted-before-completion attempts has
  precedent); ledger note required.
- **GPU P-state degrades mid-flight:** the live fix (`nvidia-smi -lgc 1200,2500`) is an
  intervention on a live run — owner call unless the block is otherwise lost.
- **Umbrella collision:** five untracked files belong to a parallel session; commit only
  uniquely-named files; never `git add -A` in the umbrella.
