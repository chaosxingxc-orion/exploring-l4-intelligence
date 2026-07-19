# Survey Router

This page routes survey material by lifecycle role. It carries no protocol rule, result table, or
copied machine count.

| Need | Route | Loading rule |
|---|---|---|
| Current gate, effective protocol, active tables/data, and machine manifest | [`current/README.md`](current/README.md) | Start here for a named survey task; follow `current/manifest.json` hashes |
| Long-lived paper census, claims, and evidence records | `registry/` | Targeted lookup only; existing compatibility paths remain manifest-routed until migrated |
| Mutable exploration for a live campaign | `workbench/<campaign>/` | Never default context and never a completion claim |
| Reviewer transaction and round history | `../audit/<campaign>/INDEX.md` | Open the campaign index first; load one exact round only for provenance |
| Superseded working material | `../archive/<knowledge-layer>/<campaign>/` | Cold; load only for a named historical/replay question |

The full placement, consolidation, and safe-move policy is canonical in
[`../AI-Collaboration.md`](../AI-Collaboration.md). The current research stage and authorization
boundary are canonical in [`../Research-Objective.md`](../Research-Objective.md).
