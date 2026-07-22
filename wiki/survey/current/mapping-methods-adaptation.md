---
artifact_id: "SF-MAPPING-METHODS-ADAPTATION-V1-2026-07-21-01"
role: "current Stage-1B methods basis; protocol input, not a review verdict"
stage1b_execution_authorized: true
h5_load_bearing_use: "WITHHOLD"
---

# Systematic-mapping methods basis and adaptation

This mapping is designed for a fast-moving AI/CS literature in which arXiv, venue-native proceedings,
versioned full text, and compound-system method paths all matter. The sources below are methodological
anchors, not decorative citations. The current protocol remains controlling wherever an adaptation is
stated explicitly.

## Method anchors

- Petersen et al., “Systematic Mapping Studies in Software Engineering,” EASE 2008,
  [DOI 10.14236/ewic/EASE2008.8](https://doi.org/10.14236/ewic/EASE2008.8).
- Wohlin, “Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software
  Engineering,” EASE 2014, [DOI 10.1145/2601248.2601268](https://doi.org/10.1145/2601248.2601268).
- Page et al., “The PRISMA 2020 statement,” BMJ 2021;372:n71,
  [DOI 10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71).
- McGowan et al., “PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement,”
  Journal of Clinical Epidemiology 2016;75:40–46,
  [PubMed 27005575](https://pubmed.ncbi.nlm.nih.gov/27005575/).
- Rethlefsen et al., “PRISMA-S,” Systematic Reviews 2021;10:39,
  [DOI 10.1186/s13643-020-01542-z](https://doi.org/10.1186/s13643-020-01542-z).

## Adaptation table

| Guideline | adopted element | AI/CS/arXiv/T1 adaptation | deviation/rationale | controlling artifact |
|---|---|---|---|---|
| Petersen | map questions to classification facets and report category frequencies | work is the deduplication unit; method path is the coding/occupancy unit; task, modality and selection-object strata retain separate denominators | no omnibus “paper count” substitutes for path-level mechanism evidence because one paper can contain incompatible paths | `protocol.md` §§1–2, 6, 9; REC-2 |
| Petersen | staged screening and data extraction | REC-0 screens every candidate; D0/D1/D2 code-on-use controls extraction depth | D2 is required only for load-bearing/direct-threat claims so Stage-1A does not pre-run Stage-1B | `protocol.md` §§4, 6, 8; REC-0/REC-2 |
| Wohlin | backward/forward snowballing with explicit start set and iteration stop | frozen seed and reviewer-known inputs may start DFS but have `query_recall_credit=false`; every edge preserves provenance | arXiv version aliases collapse to one work node, while discovery-source memberships remain many-to-one | `protocol.md` §5; canonical-work union |
| Wohlin | saturation and stopping | each iteration records new eligible works, duplicates, exclusions, inaccessible items and unresolved identities; exit follows the preregistered stop rule | “no new paper noticed” is not accepted as saturation evidence | `protocol.md` §§5, 8–9; REC-6/REC-7 |
| PRISMA 2020 | transparent flow accounting and reasons for exclusion | counts are machine-derived across discovery routes, T1 rescue, deduplication, full-text availability and final coding | the protocol is a systematic mapping rather than a health-intervention review, so effect synthesis items are not imported | `protocol.md` §§3–5, 9; flow report |
| PRESS 2015 | independent peer review of search strategy before execution | query/compiler, T1 routes and wordlist are frozen; review concerns create explicit corrections before the first discovery query | exact platform syntax is compiler-generated and tested instead of being copied manually between databases | frozen query/compiler; search-design review package |
| PRISMA-S | reproducible search reporting | exact request bytes, dates, pagination, overflow splits, retries, raw responses and access classes are logged | known-ID metadata and reviewer verification are reported separately and never counted as query recall | `protocol.md` §§3–4, 8; REC-1 and access ledger |

## Stage discipline

Stage-1B may execute the frozen mapping and produce evidence bundles. It may not run research models,
smoke tests, task metrics, headroom experiments, prototypes, candidate-card ranking, owner selection, or
reproduction-list freeze. Stage-1C owns the latter synthesis decisions; Stage-2 owns empirical tests.
