# AI Collaboration

This page is the **single complete specification for how documents are placed, loaded, consolidated,
and moved** by AI and human collaborators. The goal is that a new session can act after reading only
a very small current layer, while historical evidence stays auditable. Every other file keeps a short
route only and never copies this ruleset.

## 1. Default load and first principles

Every document in this program is written in English, and everything that enters a model context is
English: translate a non-English source before feeding it, never after. Non-English text in a mutable
document is a defect to repair at the next touch of that file; immutable records and hash-pinned
bytes are superseded by an English successor instead of being rewritten.

The default load surface is exactly three items: the client guide (`AGENTS.md` or `CLAUDE.md`) →
`wiki/Research-Objective.md` → `wiki/Project-Thesis.md`. `wiki/Per-Work-Status.md`,
`wiki/survey/current/`, and machine reports are loaded only when a task calls for them.

- Never read `wiki/Decision-Log.md` end to end, and never broadly load `wiki/20*.md`, historical
  proposal/review/response/amendment files, `wiki/audit/`, or `wiki/archive/`; to find provenance,
  go through the campaign index first, then `rg` for the exact entry.
- Current truth may exist only in stable HOT/CURRENT files. AUDIT preserves what happened, ARCHIVE
  preserves retired work products; **a patch chain, a response letter, or an amendment chain must
  never serve as active truth**.
- Numbers, hashes, and status are canonical in the current manifest, a ledger, or a release-scoped
  check report; prose cites the canon and never transcribes a parallel copy of the figures.
- Team knowledge must land in a file in the repository. Personal memory and transient AI reasoning
  are not team canon.

## 2. Document types and their single location

Every persistent document must declare exactly one role; one file can never be both "the specification
in force" and "the audit history of how the specification evolved".

| Type | Required location | Who reads it | Default load | Authority / mutability | Entry condition | Move / exit condition |
|---|---|---|---|---|---|---|
| **HOT** | `AGENTS.md` / `CLAUDE.md`; `wiki/Research-Objective.md`; `wiki/Project-Thesis.md`; `wiki/Per-Work-Status.md`; `wiki/Experiment-Assets.md` | every new session reads the first three; Per-Work and experiment assets on demand | first three only | current fact, supersede-in-place | an owner ruling, the current stage, blockers, cross-work status, or an experiment-asset authority boundary must be visible immediately | replace in place and leave one cold index pointer; never date-versioned and never a pile of qualifiers |
| **REGISTRY** | `wiki/survey/registry/` (the compatibility path `wiki/survey/sidecars/` is manifest-governed) | whoever verifies, codes, or writes from the literature | No | long-lived census/claim/evidence registration; entities are append-only and verdicts supersede explicitly | a paper FETCH or close reading, a canonical ID, or a load-bearing claim is adopted | retained across campaigns; never copied into protocol prose, an invalidating verdict carries a token, and no record is deleted |
| **AUDIT** | ordinary transactions: `wiki/audit/<campaign>/<round-id>/`; ordinal-bearing iterations: `wiki/audit/<campaign>/epoch-<N>/<round-id>/`; index = `wiki/audit/<campaign>/INDEX.md` | reviewer and auditor; AI only for exact forensics | No | round artifacts and `consolidation-receipt.json` are immutable from their first commit; the index is append-only | a reviewer submission, report, response, or sign-off is written straight to its permanent path and registered; amendments and corrections run the epoch state machine, whose only unnumbered exception is the path-pinned B8 correction | registered artifacts are never moved or rewritten; once out of active routing they are reachable only through the campaign index |
| **ARCHIVE** | `wiki/archive/<knowledge-layer>/<campaign>/` | history and reproduction questions only | No | immutable once moved in | an unregistered work product is **closed** (finished, superseded, or abandoned) and has no active dependency | permanent cold storage; only a new audit correction can reinterpret its historical meaning, and it never returns as current |
| **WORKBENCH** | `wiki/survey/workbench/<campaign>/` | the current explorer | No | mutable working knowledge, must not carry completion claims | the question is still under exploration and the rule is not yet accepted | useful conclusions are consolidated into HOT/REGISTRY, the dossier is kept for archive, and worthless scratch is not committed |
| **Engineering spec** | `docs/superpowers/specs/` | implementer and reviewer | No | bounded engineering design, versioned through Git review | a multi-step engineering change needs its scope and constraints locked first | Git history retains it once finished; the research current page does not depend on a plan or spec to be understood |
| **Engineering plan** | `docs/superpowers/plans/` | implementer | No | checkbox mutable while executing | an approved design needs decomposition into execution | it stops being a current research pointer when finished; Git preserves the history |
| **Study repository registry** | `studies/README.md`; `studies/registry.json` | owner, implementer, CI | No, engineering-task directed | umbrella tracking; only an admitted, semantically named standalone Git repo is registered | a standalone research object receives `OWNER_GO_AND_EXECUTION_CONTRACT`, freezing its semantic name and execution contract | lifecycle changes update in place; a candidate ID must never become a repo name, and no empty repo is created for an unadmitted or pre-creation sunset candidate |
| **Paper repository registry** | `papers/README.md`; `papers/registry.json` | owner, implementer, CI | No, engineering-task directed | umbrella tracking; a semantically named standalone Git repo (Stage-3, continuation entry 91) | a qualified study candidate is promoted through `OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` | lifecycle updates in place; a candidate ID must never become a repo name; an empty registry is legal and no empty paper repo is created |
| **Study experiment index** | `wiki/experiments/<study-slug>/README.md`, routed from `wiki/Experiment-Assets.md` | owner, implementer, reviewer | No, study directed | the Wiki governs experiment state and the asset graph; a record must pin the repo commit, protocol, config, data, model, and artifacts | the study is registered and its experiment contract has entered execution | conclusions consolidate into the stable current page; release/audit bytes are never written back, and a recoverable index survives study sunset |
| **Paper experiment index** | `wiki/experiments/papers/<paper-slug>/README.md` (created at the first admission), routed from `wiki/Experiment-Assets.md` | owner, implementer, reviewer | No, paper directed | the Wiki governs Stage-3 experiment state and the asset graph; a record must pin the paper commit, protocol, data, and artifacts | the paper is registered and promotion is complete | conclusions consolidate into the stable current page; release/audit bytes are never written back |
| **Check report** | `docs/checks/<campaign>/<release-id>/` | gate tooling and verifiers | No | immutable once a release cites it | a repeatable check produces a platform- or version-specific result | new release, new directory; no cross-platform sharing of a last-writer-wins filename |
| **Executable rule** | `scripts/` | CI, operator, reviewer | No, executed, not read through | normal code lifecycle, tests first | a prose rule becomes mechanically verifiable | tests change with the rule; prose points at the checker and never maintains a second implementation |
| **Ephemeral scratch** | **Not committed** | the current session | No | no authority | temporary reasoning, drafts, one-off output | distil the valuable conclusions with provenance before handoff; delete or expire the rest |

Classify a new document against the table above before creating it; never drop it into the `wiki/`
root and wait for a future cleanup. Existing path-pinned legacy files are a compatibility exception:
keeping the original path does not make them active, and they must appear in the cold inventory of
the AI context manifest.

Engineering repositories and asset bytes use three layers of authority: `studies/<semantic-slug>/`
(Stage-2) and `papers/<semantic-slug>/` (Stage-3, after promotion) are standalone Git/GitHub
execution repositories, the umbrella Wiki is the governing authority for experiment lifecycle and
asset relationships, and `SPEECHRL_DATA_DIR`/MLflow hold large data, weights, raw output, and run
objects. The Wiki must index the URI, ID, and hash of those bytes but must never copy a large asset.
The W1–W4 `projects/` repositories do not automatically own any new study; only a capability that is
stable and genuinely reused across repositories is promoted into `common/`.

## 3. Six-step lifecycle

Every campaign uses the same pipeline:

1. **Capture** — capture the conclusion, reasoning summary, purpose chain, provenance, invalidation
   condition; anything not yet stable stays in Ephemeral scratch, or enters the WORKBENCH of a new
   campaign when it must persist.
2. **Classify** — before committing, assign exactly one role, the authority source, the readership,
   and the exit condition. A reviewer transaction is classified as AUDIT at this point; it is never
   created in an active directory and moved later.
3. **Work** — drafts evolve in the WORKBENCH; an accepted effective rule supersedes in place, only
   in the stable CURRENT file. A current file must be self-contained and must never need the
   workbench or the archive to be understood.
4. **Consolidate** — distil the log and its corrections into one effective specification plus a short
   status, update the current manifest, and delete the duplicated statements from the active layer. A
   correction in design means a new AUDIT correction plus an in-place CURRENT repair, and never a
   change to old audit bytes.
5. **Release / Audit** — review freezes, submissions, reports, responses, corrections, and sign-offs
   go straight to a permanent AUDIT path and are registered; check output goes to its own Check
   report directory. A release cites only hash-pinned output.
6. **Archive / Expire** — at campaign close, distil first, then clear the manifest and references,
   and move the qualifying work products last; worthless scratch expires uncommitted. The next
   campaign uses a fresh WORKBENCH/AUDIT namespace and never reuses an old filename.

Mapping to the older vocabulary: Draft→Work, Effective→the CURRENT page after Consolidate, Review
freeze→Release / Audit, Correction→a new AUDIT record plus an in-place CURRENT repair, Campaign
close→Archive / Expire, Next campaign→a fresh Capture. This mapping does not change audit
immutability.

## 4. Mandatory consolidation and move triggers

Consolidate immediately when any of the following happens first:

- a **third amendment or correction** is about to appear;
- a protocol, router, or HOT file **exceeds its context budget**;
- a reviewer Gate MAJOR closes, or a **reviewer Gate MAJOR changes an executable contract**;
- **handoff ambiguity**: reading the current protocol plus status still does not determine the next
  action;
- a **stage/release boundary**, campaign verdict, sign-off request, or publication release is reached;
- **competing active claims** exist: two active files give competing statements for the same current
  field.

A third audit correction may preserve history, but **the third correction must be folded in
immediately** to the effective spec. Correction ordinals count only within one **consolidation
epoch**, and the only legal values are 1–3; within one epoch **a fourth correction must never be
added**, and ordinal 4 is never legal. To keep correcting, Consolidate first, then create the next
`epoch-<N>` and restart ordinals at 1.

Ordinary review transactions still use `wiki/audit/<campaign>/<round-id>/`; the only permitted
unnumbered fixed correction is the path-pinned B8 file
`wiki/audit/system-first-stage1a/round-12/stage1a-readiness-correction.md`. Every other new
amendment or correction uses `wiki/audit/<campaign>/epoch-<N>/<round-id>/<name>-<ordinal>.md` and
carries LF-only front matter whose exact schema is
`schema/campaign/epoch/ordinal/kind/effective_spec/effective_spec_version/effective_spec_sha256`,
where schema=`ai-context-audit-iteration-v1`, and whose metadata must agree exactly with the path
and with this epoch's receipt.

Each epoch's `epoch-<N>/consolidation-receipt.json` is a non-default-load AUDIT artifact, immutable
from its first commit, whose exact schema is
`schema/campaign/epoch/effective_spec/effective_spec_version/effective_spec_sha256` with
schema=`ai-context-consolidation-receipt-v1`. Both the artifact and the receipt must enter the audit
registry with a pinned Git blob, and the stage-0 blob raw bytes must equal the trusted worktree
bytes. Epochs increase from 1 without gaps within each campaign; within each epoch the ordinals are
unique and contiguous over 1..max, with max≤3. The highest epoch receipt must bind the
`wiki/survey/current/protocol.md` recorded in the current manifest, with version equal to its front
matter and sha256 equal to its staged raw bytes. Before opening a new epoch you must commit the
receipt first, then append the registration, raise the immutable registry prefix count/hash anchor
in step, and pass the immutability check; the existence of a new epoch is therefore proof that every
earlier epoch has a complete registered receipt chain. A previous epoch may be consolidated early at
ordinal<3 because of another mandatory trigger. Forgery, a missing number, a duplicate, an
unregistered artifact, a repin, or dirty bytes all fail closed. Consolidation is not one more layer
of explanation: it rewrites CURRENT in place into a single, complete specification that depends on
no patch chain.

Any append to the audit registry must sit in the same transaction as the complete prefix count/hash
anchor of `scripts/checks/ai_context_inventory.py` and a fresh immutability report; stage the
registry and anchor first, generate the report, then stage it, and finally run the builder `--check`
and the zero-write assertion. Appending only to the registry tail and leaving the old anchor for the
next task to repair is an illegal state.

An ARCHIVE move triggers when a work product is "superseded and absent from the current manifest";
when it is safe, complete it in the same commit as its replacement. When it is not safe, record an
explicit closeout blocker and resolve it before sign-off; never force the move. Registered AUDIT is
the exception: it is never moved, only removed from active routing.

Since 2026-07-28 there is also a **sunset channel** (owner ruling, Decision-Log continuation entry
75): a superseded work product with no active reference may be deleted from the worktree instead of
moved, with its historical bytes preserved by Git. Its preconditions and safety gate are identical to
ARCHIVE; every deleted path must record its blob hash and recovery command in the campaign's sunset
ledger, and narrative records are distilled into the sunset digest first. Registered AUDIT bytes do
not change, and their worktree entries may be deleted only when the immutability check verifies
reachability through Git history. Pre-convention loose files and zero-reference reports under
docs/checks, and zero-reference finished plans under docs/superpowers/plans, are eligible for this
channel.

### Pre-move safety gate (mandatory)

1. Read the regular-file path, mode, and Git blob from the **stage-0** Git index; worktree bytes must
   equal that blob, and a move decision may never be made on a dirty file or an unbound snapshot.
2. The source path must not be in the **audit registry** or the **current manifest**; registered
   AUDIT is never moved.
3. On the stage-0 graph, check every **inbound reference** from HOT/CURRENT and registered AUDIT, and
   confirm that no active script depends on the old path; references, plain text, relative and
   root-relative paths, and encoding variants are all in scope.
4. Update every live pointer plus the manifest and hashes first, keeping a deterministic plan of
   source, destination, mode, and Git blob; accept only "entirely at the source" or "entirely at the
   destination", because partial/both-path states fail closed.
5. Use `git mv`, and never edit content to add an archive banner. After the move, prove that the
   source is absent, the destination is present, the mode and blob are identical, and no active
   old-path reference remains.

## 5. Records, hashes, and release

- Five fields for persistent knowledge: **conclusion / reasoning summary / purpose chain /
  provenance / invalidation condition**. Being unable to write the purpose chain is a stop signal;
  recording a conclusion without the reason behind it does not qualify.
- New Decision Log entries use ADR form: Context / Decision / Rationale / Consequences / Supersedes.
  Old entries are append-only; a change is written as a new ADR.
- Every load-bearing status in the hot layer states "what is locked, in service of which higher
  goal". Before a session ends, purpose-layer conclusions, load-bearing intermediate conclusions,
  and unfinished intentions must be written down in the correct layer.
- Evidence hashes are canonical as the **git blob bytes** of `(commit, sha256)`; worktree CRLF is
  only one variant of those bytes.
- Before release, complete the adversarial internal review, the purpose-chain check, the
  context/manifest/check gates, and the archive scan. The true source of the Wiki is `wiki/*.md` in
  the repository; `scripts/wiki-sync.sh` publishes only after explicit authorization, and the web
  version is a mirror only.
