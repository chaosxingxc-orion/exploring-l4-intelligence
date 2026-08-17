# Owner GO — kb-construction runtime-intersection supersession (2026-08-16)

Ruled by the owner conversationally on 2026-08-16 night; recorded by the implementer the same
night. This record supersedes ONE clause of the frozen `kb-construction-sample` receipt (owner
decision 2026-08-13, frozen at study commit `bea16af`): the clause "runtime evaluation splits
must never intersect this set".

## Ruling

The intersection prohibition is superseded for **discovery-tier** blocks, under two binding
conditions:

1. **No artifact constructed from these 34 calls' gold annotations may enter any runtime path
   of a block that evaluates on them.** Construction-side gold use remains permitted exactly as
   the original receipt allows. This condition becomes machine-checkable when the E1' legality
   fields (`span_source` / `reference_source` / `legality_tier`) land; until then it is enforced
   by registration review.
2. **Any block whose evaluation split intersects the 34 stays discovery-tier.** Confirmatory
   splits still must never intersect this set; that half of the original clause stands.

## Effect

The n=44 earnings21 discovery block (the full frozen discovery split, hash
`fcc1b0bc55432d02347dcdf730c6bcef561a9b0ad9605c45b367e1ed3da5d69e`) is admitted for
registration once its other gates pass (N0 power analysis; N1 routing gate per the registered
MUST-NOT-FLY line; E0' flight protection).

## Deferred

The demonstration-bank lane (DEMO, plan doc §7) constructs from these calls' gold — permitted
construction-side use. Its future *runtime* use on other calls requires its own legality-tier
classification at that screen's registration; nothing here pre-grants it a legal tier.

Rationale context: the route the original clause protected (the cross-call error-pattern KB)
was closed by measurement on 2026-08-14; the 34 calls are already discovery-exposed
(`SAEA-BENCH-kb34-floor`, `SAEA-TOOL-lexicon-v2`); and the earnings21 discovery split is the
whole corpus, so without this ruling no earnings21 scale exists.
