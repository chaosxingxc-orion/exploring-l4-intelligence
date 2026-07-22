---
title: "Stage-1B bounded three-round execution snapshot"
date: 2026-07-22
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
role: "WORKBENCH execution receipt and synthesis; no novelty verdict"
---

# Stage-1B bounded three-round execution snapshot

## Conclusion

The owner-directed bounded scan is complete and broad scanning stops. Three deterministic,
non-overlapping 1,000-paper rounds were drawn from the frozen 20,727-ID D0 union. The final v5
abstract policy selected 251 works for PDF reading, deferred 1,561, and excluded 1,188. All 251
selected PDFs were downloaded, extracted, and assigned a final full-text decision; unresolved = 0.

After nine page-cited audit overrides, the retained roster is **159 unique works**, far below the
1,000 maximum: **10 core speech/audio control paths, 22 instruments/trained direct comparators,
119 adverse/boundary records, and 8 repository-verified non-speech transfer paths**. Ninety-two
full-text candidates were dropped. The cap is a maximum, not a quota.

This is a sampled method/evidence portfolio. It does not support exhaustive REC-0 closure,
corpus-exhaustion, prevalence, or novelty claims over the remaining D0 union.

## Replay and artifact receipts

The D0 source SHA-256 is
`afc3d85eab383f81c96d293b13d053767500baec485c89ce03aeff32f3425883`; the dataset lock SHA-256 is
`1790b43c0c2c9ba8b1a3d1ce3d1588d3aa84e63f7d680cef78e20da7adf70c1f`.

| Artifact | Rows / bytes | SHA-256 |
|---|---:|---|
| v5 round 1 abstract ledger | 1,000 / 3,039,258 | `ca121f477e2109336dfd9a5519626e4281365f4cacf12a7cd19fea2081352d65` |
| v5 round 2 abstract ledger | 1,000 / 3,090,933 | `db0cae386f7a986a7c6d16c79d54fac8f253ee39035cd54beb505742c5b9deca` |
| v5 round 3 abstract ledger | 1,000 / 2,979,318 | `978bc9e920b4e5e91cca2dbfec2118f734693bfa20c34bd582a48adf081360cc` |
| final full-text triage | 251 / 1,322,956 | `91d69b01d04f430bbf9507f8a382f3df4313ed84e64e18a5a532616f6e76d487` |
| repository verification cache | 145 canonical repos / 90,478 | `d5f72fb41d6d474ee70fee694b6aa66454bb222ee97462586768f3282dcb177a` |
| retained roster | 159 / 858,027 | `120716473bb438ad33739a6837226c5434d8f5f4bfd377ec08d83e9f5275b1a3` |
| metadata-only Git registry | 159 / 424,030 | `363f953e20a0100512ce12cf70b8a43081b693a767062ab820e1787f5762aee5` |
| generated registry views | 159 / 106,194 | `82c9a63342f2043e8d36a8f87a1b0f53cca5ca13751f1d463cb2b1426b20192e` |
| append-only full-text ledger | 716 / 315,654 | `c5843e016357f3ed33efabe1a5cee358a6e61c92aa13279816f7cb8a3681f67e` |

The 251 PDFs total 1,354,302,168 bytes and 5,388 pages; extracted text totals 19,259,262 bytes. All
159 retained e-prints are present externally and total 735,352,298 bytes.
PDF/e-print/extracted-text bytes stay outside Git. Earlier v1-v4 policy caches and their extra
downloads are retained externally as audit evidence but are not roster or registry members.

## Why the policy changed during execution

The abstract→PDF→full-text pipeline caught three false-positive mechanisms before consolidation:

1. a bare `ASR`/speech mention in a visual or safety abstract was mistaken for a speech task;
2. `hate speech`/`counter-speech` text tasks were mistaken for acoustic speech;
3. AIME or spoken-capable agent benchmarks were mistaken for proof that the paper's primary object
   was acoustic speech.

The final v5 rule requires acoustic evidence in the title/contribution plus any dataset corroboration;
generic local datasets cannot create speech-primary status. Full text also distinguishes a genuinely
frozen/no-update path from a paper that merely says “test time.” Nine trained methods with frozen
subcomponents were downgraded from core to instrument using explicit page evidence in
`2026-07-22-bounded-fulltext-audit-overrides.json`.

## Speech task and local-data result

Sixty-five of the 251 full-text works are primary speech/audio objects. In the retained roster,
23 primary-speech works have an exact local-lock dataset match. Exact task-compatible cells include:

- ASR × LibriSpeech: 9 retained records;
- speech translation × CoVoST2: 1; speech translation × FLEURS-R: 1;
- audio generation × MMAU-mini: 2;
- TTS × Seed-TTS-Eval: 1.

Other exact-name matches remain `REQUIRES_SPLIT_REVIEW`; for example, a paper carrying both ASR and
SER tags does not make LibriSpeech an SER dataset. Directory presence is never promoted into a result
reproduction claim.

## Non-speech open transfer result

The repository pass normalized 145 paper-linked candidates: 19 met the structural open-source gate,
7 were inspectable but reproduction-incomplete, 26 lacked a resolved license, 6 non-GitHub links need
manual handling, and 87 were unreachable or malformed. Only eight papers both met the repository
gate and preserved a transferable full-text signal→action path:

- DiffusionAgent — feedback-based expert routing for image generation;
- Memento — context/memory adaptation without base-model fine-tuning;
- PRInTS — reward modeling for long-horizon information seeking;
- MoRL — open motion understanding/generation reasoning path;
- VideoSEAL — separate evidence acquisition from answer authority;
- Vision-OPD — fine-detail visual policy/self-distillation comparator;
- visual-redundancy-controlled parallel decoding;
- See Only When Needed — context-aware attention intervention.

These are references/components, not claims that speech transfer has already succeeded. Upstream
execution is still unrun; repository status proves inspectable structure, license, source, README, and
environment specification, not metric reproduction.

## Purpose chain

The retained roster converts a 20,727-item retrieval union into a manageable evidence portfolio for
Stage-1C problem selection and reproduction-first Stage-2A preparation. Core + local task-compatible
rows identify executable speech slices; instruments provide metrics/baselines; negatives provide
falsifiers and abort criteria; open transfer rows provide inspectable components.

## Provenance and invalidation

The replayable scripts live under `scripts/survey/`; PDF/e-print URL, attempt, byte, hash, and external
path receipts remain in the append-only full-text ledger. The long-lived paper records are under
`wiki/survey/registry/` and deliberately omit abstracts, snippets, local paths, and full-text bytes.

This snapshot must be superseded if the frozen D0/dataset-lock bytes change, a paper revision changes
the coded path, repository/license status changes, a page-cited audit override is reversed, or the
owner reopens scanning. No such event silently mutates the 159-row registry.
