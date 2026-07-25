# Agentic calibration R2 codebook consolidation

## Object extraction

For `EMPIRICAL_EXTRACTABLE`, extract every material run configuration, its observations and its
dataset nodes. A change to dataset revision/split, model/access, input condition, intervention or
budget creates a new run cell. Multiple metrics from one run are observations, not duplicate cells.

When a controlled baseline-to-intervention comparison closes, create `paired_comparisons`; otherwise
select exactly one typed absence reason. Source-backed dataset provenance or validation creates a
dataset edge. Semantic similarity without provenance is not lineage.

Every evidence-bearing object uses precise typed coordinates. Title-only and abstract-only locators
cannot carry empirical objects.

## Compiler-owned identity

Coders emit local object IDs solely for within-response references. They never emit agreement keys.
The compiler:

1. binds each locator to the frozen rendition SHA256 plus typed coordinate;
2. derives `SA-<hash>` source-anchor IDs;
3. resolves dataset/run/observation/comparison/edge references to compiled identities; and
4. derives `OBJ-<hash>` segmentation signatures from paper, object type, anchors and the documented
   normalized identity tuple.

No fuzzy, semantic or post-hoc matching is permitted. A caller-authored `object_match_key` is a raw
schema error.

## Agreement denominator

For each paper/object type, segmentation uses the exact union of compiled keys. A key emitted by only
one coder is a disagreement in segmentation and in every applicable critical-field gate. A field
denominator can be zero only when both coders emitted zero objects for that class. Therefore unmatched
objects cannot be hidden as `NOT_CALIBRATED`.

## Reference, borrowing, paper support and anchor

- `REFERENCE`: transfers neither protocol nor results. Paper-visible support may still be recorded
  as evidence without granting candidate status.
- `BORROW_PROTOCOL`: requires source/target variables, preserved decision structure, source
  locators, rejection condition and observable rejection evidence.
- `paper_reproduction_support`: records only facts observable in supplied paper bytes. It may be
  `OPEN_WITH_BLOCKERS` when revision, entrypoint or terms are not stated.
- `REPRODUCTION_CANDIDATE`: requires at least one `CLOSED_PAPER_SUPPORT` record with no blockers.
- `local_reproduction_readiness`: reviewer-only repository/assets/loader/terms state.
- `REPRODUCTION_ANCHOR`: impossible in calibration; later requires closed paper support, local
  closure and 100% second review.

## Scope boundaries

Direct Agentic scope requires observable decision plus action/tool behavior. Specialized Duplex
cores, trained-controller dependencies and non-empirical boundaries cannot create Agentic experiment
cells, reproduction anchors or branch primaries. Knowledge, Skill and Memory are capability assets;
system/carrier and training-free control remain separate dimensions.
