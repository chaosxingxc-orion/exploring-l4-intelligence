---
title: "Owner GO: sampled baseline-reproduction execution (R0.1 plan P1/P2 entry)"
date: 2026-08-08
authority: "owner session directive (Claude Code /goal, 2026-08-08); the directive is preserved in the owner's original characters, with an English gloss, in the 'Owner directive' section below"
scope: "study speech-aware-evidence-acquisition, Stage-2A"
---

# Owner GO — sampled baseline reproduction (2026-08-08)

## Owner directive (verbatim, glossed once)

The directive this record rests on is kept in the owner's original characters as the quoted source,
with an English gloss beside it:

`«完成规划好的实验和工作，完成数据集采样和相关工作基线的复现，模型采用Qwen3-omni，如果有涉及到知识或者向量化的，可以考虑用本地的生成式embedding模型 | 多轮自检下，程序无误，工程可复现»` ("Complete the planned experiments and work; complete dataset sampling and the reproduction of the related-work baselines; use Qwen3-omni as the model; where knowledge or vectorization is involved, a local generative embedding model may be considered | under multi-round self-check, the program is defect-free and the engineering is reproducible")

## Decisions

Acting on the owner session directive quoted above, this record lands the following decisions:

1. **Adopt** the study repo's `docs/readiness/2026-08-07-r1-replan-reproduction-plan.md`
   (P0–P4, including the four-construction abstraction framework, the sample-once manifest
   policy, and the T-series analogue track) as the execution form of the R1 re-plan
   (the composite of HANDOVER options 2+3). Sampling is already frozen under the
   sample-once policy (manifest anchor `c5130274…`).
2. **Execution sequence**: the first model contact is `SAEA-E-001-r0-smoke` (the smoke
   already fixed by the R0 runbook; bare-core; e22 dev subset10); afterwards execute in
   P2 order on the visible carriers (the three R4 arms first, whose samples are exactly
   the frozen dev subset10). Every contact still requires its own `ExecutionPlan` +
   exposure pre-registration row + fail-closed gate — this record waives no machine
   enforcement whatsoever.
3. **Model selection**: the frozen core is Qwen3-Omni (lock key
   `qwen3-omni-30b-a3b-instruct-gguf`, llama.cpp receipt-pinned runtime). Components that
   involve knowledge construction or vectorization (T1/T2 retrieval and the like) may use a
   **local generative embedding model** as a pinned tool-level component (logged, hash-carrying,
   holding no answer authority), on the same footing as a deterministic retriever (BM25);
   final answer authority always stays with the frozen core.
4. **Known boundary**: the D/F-family carriers (audio2tool, voiceagentbench, big-bench-audio
   and others) have no `speech-aware-*` lock profile yet and are invisible to the gate — the
   real contacts of P1/R2/R5 are not executed until the lock amendment lands (through the
   umbrella's formal path); the engineering scaffolding goes first. That amendment needs its
   own separate owner data-identity decision and is not granted implicitly by this record.
5. **Self-check discipline**: dry-run validation always uses a separate run-id namespace
   carrying the `-dryrun` suffix (a real run-id's attempt metering is never consumed by
   validation); a dry run must pass before every real run; engineering reproducibility is
   judged by the manifest, the receipts, and fixed seeds.

Recorded by: the implementer (Claude), under direct owner instruction. Audit links: the study
repo's complete `docs/readiness/` set plus the corresponding rows of `docs/exposure-ledger.md`.

---

**Language conversion (2026-08-25).** Re-issued in English with terms, scope, dates, and authority
unchanged; content is preserved throughout — this is a language conversion, not an edit. The owner
directive itself is not translated away: it stays verbatim in its original characters above, glossed
once, and the YAML `authority` field now points at it instead of carrying it inline. Pre-conversion
bytes are Git blob `532d726cda342507fd5629821da82d364840b9fa`; the conversion is recorded in
`wiki/Decision-Log-2026-08.md` continuation entry 95.
