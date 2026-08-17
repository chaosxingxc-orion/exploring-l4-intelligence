# OWNER_GO_AND_PAPER_EXECUTION_CONTRACT — meeting-minutes-agent

Date: 2026-08-17. Status: **PROVISIONAL** — the owner directed the scaffold to be stood up
immediately, then ruled (same session, later message) that the final go/no-go on opening this
topic awaits the 2026-08-17 meeting-dataset and methods surveys and a joint owner analysis. No
engineering work proceeds in the repository until that final decision; the scaffold stands ready
and is fully reversible (registry removal + checkout deletion). Repository:
`papers/meeting-minutes-agent/` (independent Git repository, umbrella-ignored). This record is
the machine-checked authorization behind the registry entry in `papers/registry.json`.

## Owner authorization (translated from the owner's Chinese instructions, 2026-08-17 session)

1. "This direction is a highly valuable agent scheme. Stand it up in its own engineering
   directory, treat it as a research topic in its own right, and place it under `papers/`."
2. On my governance hesitation, reaffirmed: "Break free of the previous framework's constraints;
   a separate engineering directory carries this topic." (Direct admission by explicit owner
   order — this supersedes, for this object only, the promote-from-a-qualified-study-candidate
   default of Decision-Log continuation entry 91. The default remains in force for every future
   admission.)
3. Scope rulings, same session:
   - The **interleaved listening, spelling and revising** agent scheme (originating in the SAEA
     study's design work, e.g. its 2026-08-10 readiness note) **merges into this topic** — its
     value and research content unify with the AI meeting-notes agent.
   - This topic is a **standalone agent research object** solving AI Meeting Notes academic
     problems. It is NOT framed as "knowledge injection vs memory access"; it is a new scheme,
     distinct from the knowledge-injection study.
   - **Knowledge injection remains with the SAEA study and continues on non-meeting
     datasets/tasks only.** SAEA builds nothing further on meeting-notes-class data; meeting
     corpora belong to this topic.

## Research object

An AI meeting-notes agent over a frozen speech-capable omni core: speaker decomposition,
per-speaker content extraction, coreference and relation resolution, and an episode-local
keyword/glossary table built and maintained during the meeting and statically injected back into
the prompt — integrated with the interleaved listening/spelling/revising control scheme — to
produce speaker-attributed records, minutes, and meeting QA.

## Charter constraints

- **Fresh start**: this repository is deliberately not bound by the SAEA study's probe framework,
  exposure apparatus, or experiment ladder. Assets are imported from the umbrella or SAEA only by
  explicit recorded decision (first recorded import: the interleaved listening/spelling/revising
  design lineage, per owner ruling above).
- **Program-wide invariants that do apply**: frozen core, training-free (no parameter updates);
  English-only documents; no data/weights/audio in Git; paid API spend = 0; human speech and its
  linguistic content only.
- **Speaker-dimension information is core and mandatory** (owner ruling, same session):
  diarization, within-meeting speaker clustering and attribution state — including pinned
  frozen speaker-embedding tools — are episode-local working state, in scope. The SAEA-context
  deferral of speaker-embedding retrieval applied to that study's knowledge-supply mechanism
  only. Episode-local glossary and speaker state are in scope; only **cross-meeting
  persistence** requires a separate owner decision before any implementation.
- Carriers, evaluation protocol, and design docs are fixed by the topic's own first design
  records, informed by the 2026-08-17 surveys
  (`wiki/survey/workbench/2026-08-17-meeting-agent-direction/`).

## Registry linkage

Registry entry: `papers/registry.json` → name `meeting-minutes-agent`, admitted 2026-08-17,
status ACTIVE, authorization record = this file. The paper workspace checker
(`scripts/checks/paper_workspace_check.py`) was extended from the zero-state gate to admission
mode in the same change set (paired policy + oracle + tests).
