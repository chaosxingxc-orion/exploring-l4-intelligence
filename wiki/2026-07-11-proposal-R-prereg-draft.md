---
title: "METHOD-G1 Preregistration — Proposal-R (retrieval causality), Step-2"
date: 2026-07-11
stage: 1-problem-definition
status: "DRAFT — owner signature required. Phase-A 140-cell run + Phase-B confirmatory run BLOCKED until signed."
gate: METHOD-G1 (single-question preregistration; follows METHOD-G0 ruling, Decision-Log 续12)
primary_question: Proposal-R
companion: [2026-07-11-stage1-audit-response-and-rulings (§4 G0 tree), 2026-07-11-adversarial-review-of-stage1-audit-response (§6 Proposal-R sketch + ρ critique + equivalence-margin demand), 2026-07-10-step2-grid-draft (frozen Phase-A arm space), 2026-07-11-group-split-statistics-design (split/cluster-bootstrap/locked-holdout), Research-Proposal-Template]
supersedes_grading: none (append-only; Stage-1 evidence stays hypothesis-grade)
---

# METHOD-G1 Preregistration — Proposal-R (retrieval causality)

> **What this is.** The single-question preregistration the reviewer (`…adversarial-review…` §6.4, §8 Gate-D)
> and owner (Decision-Log 续12 ③) demanded before any Step-2 confirmatory run — freezing ONE primary question,
> its primary + replication datasets, arms, cluster units, metric, SESOI, equivalence margins, multiplicity
> family, and the two test surfaces. **Nothing here is a result.** Sign §10 before the Phase-B confirmatory run;
> the Phase-A dev sweep is exploratory (§6) and may run once §10 items 1–2 + 5–7 are signed and G2 (real-runtime
> E2E green, all control arms built) passes.

## 0. Front-matter

```
project: exploring-l4-intelligence / W1 (speech-mllm-training-free-rl)  ·  study: Proposal-R
owner: <owner sig required>  ·  date: 2026-07-11  ·  status: planned  ·  version: v0.1-DRAFT
mode: confirmatory (Phase-B locked holdout) atop an exploratory screen (Phase-A dev)
```

## 1. Research idea & falsifiable hypothesis

**Primary question (Proposal-R, verbatim from G0 tree / Decision-Log 续12).** Under a frozen generator
(Qwen3-Omni-30B-GGUF), an audio-only / own-ASR query, source∩eval = ∅, and an answer-scrubbed CLEAN KB,
does speech-keyed retrieval deliver a **preregistered end-to-end improvement over no-retrieval and over
random retrieval**, and does **oracle retrieval prove the bottleneck is actually retrieval**?

- **H1 (primary).** `Δ_e2e = metric(best-retrieval) − metric(no-retrieval) ≥ SESOI`, paired-cluster-bootstrap
  95% CI **LB > 0** on the locked holdout. Refuted by CI LB ≤ 0, point < SESOI, or a §5 equivalence kill.
- **H2 (relevance).** `metric(best-retrieval) − metric(random-retrieval) ≥ SESOI`, CI LB > 0 (refutes the mere
  extra-token / prompt-length effect).
- **H3 (bottleneck).** `metric(oracle) − metric(no-retrieval) ≥ SESOI`, CI LB > 0 (if false, the reader cannot
  exploit even perfect context → bottleneck is not retrieval).

**Co-primary estimand = ABSOLUTE delta** (`Δ_e2e`), never a ratio. ρ = `(R_arm−R_noretr)/(R_oracle−R_noretr)`
is **secondary only** (Decision-Log 续12 ③; reviewer §6.3): ratio of **aggregate** improvements (not a mean of
per-item ratios), same cluster-bootstrap draw, Fieller/joint-bootstrap CI; **denominator policy pre-registered**
— NO filtering on `R_oracle−R_noretr>0` (that conditions on favorable headroom → upward bias); if the
denominator CI crosses 0, ρ is reported `unstable/undefined`, never forced or sign-flipped.

## 2. Primary + replication datasets (two test surfaces)

Chosen from the frozen Phase-A four (`phase_a_cells.PHASE_A_DATASETS`). Confirmatory claims are restricted to
these two; the other two stay exploratory (§6).

- **Primary = `squtr`** (K9 native spoken-query retrieval). **Justification:** the only Phase-A dataset with
  **native qrels**, which uniquely enables the reviewer's mechanism decomposition — R@k/MRR/nDCG@10 (retrieval
  quality) measured on the **same items** as the end-to-end delta, so H1's gain is causally attributable to (or
  dissociated from) retrieval quality, and **oracle is exactly defined** by the qrels-positive passage(s).
  Cluster unit = **query** (clean+SNR renderings share a group), G-ID `item_id.split("|")[-1]` (split design §2.5).
- **Replication = `heysquad`** (extractive spoken SQuAD QA — **different structure:** passage-grounded, no native
  qrels). Directly instantiates the "**answer-scrubbed KB**" clause: KB built `scrub=True` (mandatory; roster
  note + `heysquad.py` LEAKAGE WARNING). Oracle = gold **source passage**; random = a random scrubbed passage.
  Cluster unit = **SQuAD passage** (G-FIELD `hash(meta["context"])`; T7 warning — group derivation may READ
  context, delivery must never inject it).
- **Not confirmatory (Phase-A exploratory breadth only):** `SQuAD-zh` (language axis), `vocalbench-knowledge`
  (open QA) — promotable to Phase-B only via the §6 winners protocol, never a standalone confirmatory claim.
- **Primary metric** = the end-to-end answer score (containment-EM / accuracy per `metrics.score`).
  **Sign-off blocker (§10):** `squtr`'s Step-1 score is `None` (diagnostic-only) — its end-to-end reader metric
  must be frozen before the lock (recommend containment-EM of the generator's answer given delivered passages;
  nDCG@10 becomes the mechanism secondary). If owner rules squtr retrieval-only → primary = **nDCG@10** (oracle
  = perfect qrels ranking).

## 3. Survey & positioning (brief)

Direction/baselines argued in `2026-07-09-step2a-mmknowledge-survey.md` (105-candidate grid) + grid draft.
**Novelty delta:** unlike text/vision RAG causality studies, Proposal-R isolates whether **speech-keyed**
(audio-direct) retrieval — not an ASR→text cascade — is the load-bearing lever under a strict audio-only /
own-ASR boundary. Closest prior: Hearing-More retrieve-then-select (grid §2); this adds the no/random/oracle
causal ladder + a preregistered equivalence-margin kill.

## 4. Boundary & repro manifest (all invariants below now implemented — cite ticket #25, Decision-Log 续12/续13 "#25 Phase-A seven-item P0 fixes VERIFIED")

- **kb CLEAN gate.** `kb_retrieve.load_source` refuses an unclean source; `heysquad` KB built `scrub=True`
  unconditionally (else every heysquad cell is inadmissible by construction).
- **eval_manifest ∩ = ∅ machine invariant.** KB-source pool ids and eval item-ids structurally disjoint,
  enforced as a machine check (closes the audit's "prose-not-invariant" gap).
- **Own-item exclusion.** `run_mock._exclude_own_item` drops any hit with `provenance.from_item_id` == the
  current item, applied both pre- and post-`apply_retrieval_kind` (a self-hit never eats a final-k slot).
- **Retrieved-passage logging.** `run_mock._record_retrieved` persists `{source, from_item_id, sim, text}` per
  item → the IB-Guard can be re-run over what was ACTUALLY retrieved, not just the score.
- **Information-Boundary-Guard (query arms).** audio-direct / own-ASR / HyDE paths never see the gold
  transcript or answer; the **gold-transcript arm (§5) is the ONLY IB-violating arm**, quarantined to
  upper-bound-only reporting.
- **Strict no-RL invariant.** `assert_no_adaptive_logic` rejects any adaptive/reward/selector field name at
  every run — a MockConfig is a fixed pipeline (no reward selection, gating, or per-item branching).
- **Provenance block.** `provenance.collect_provenance` stamps repo SHA + dirty flag, `dataset_revision`,
  `manifest_hash` into every result JSON; fixed `DEV_SEED`/`TEST_SEED`; `reproduce:` line + MLflow id embedded.
- **Locked-holdout access control (#26):** test membership under `_repro/LOCKED_HOLDOUT/`, readable by exactly
  ONE consumer — the final `--confirmatory` scoring pass (stamps `locked_holdout_touched:true` + `ACCESS_LOG.md`).
  No arm/prompt/threshold selection may read it.

## 5. Mechanism controls (MUST — the causal ladder)

Every control is a pre-named arm; the four **not yet in the 35 exploratory arms must be built + E2E-green (G2)
before the confirmatory run** (own-ASR and long-context already exist in `run_mock`).

| control arm | definition | role / kill it feeds |
|---|---|---|
| **no-retrieval** | frozen generator, audio-only + fixed task prompt, **no KB injection** (= Step-1 `run_baseline` cell) | H1/H3 baseline comparator |
| **random-retrieval** | same pipeline, k passages drawn **uniformly at random** from the CLEAN pool (not by similarity) | H2; feeds *retrieval-lever-dead* kill |
| **oracle-retrieval** | inject the gold-relevant passage(s) — squtr: qrels-positive; heysquad: gold source passage | H3; feeds *bottleneck-not-retrieval* kill; ρ denominator |
| **long-context stuffing** | stuff a large fixed pool, no ranking cut (`retrieval.kind="long-context-stuffing"`) | separates "more tokens" from "relevant tokens" |
| **gold-transcript** | query built from the **gold human transcript** (IB-violating) | **upper-bound ONLY**; ASR-penalty ceiling; never a deployable claim |
| **own-ASR cascade** | query from the model's OWN ASR transcript (`asr-transcript-text-key`), deployment-compliant | the deployable text-query path; gap (gold-transcript − own-ASR) = ASR-quality penalty |

**Kill rules with PRE-REGISTERED equivalence margins (TOST; Δ_eq = SESOI/2).** The reviewer rejected "random ≈
best" without a margin (§6.2), so `≈` = an equivalence test (both kills hard; if met, reported as valid negative
results per Template §2, not reworked):

- **Retrieval-lever-dead** — fire iff best does NOT beat random by ≥ SESOI (H2 CI LB ≤ 0) AND TOST equivalence:
  90% CI of `(best − random)` ⊂ `(−Δ_eq, +Δ_eq)`. → lever dead; stop optimizing retrieval.
- **Bottleneck-not-retrieval** — fire iff `(oracle − no-retrieval)` is TOST-equivalent to 0 within `±Δ_eq`
  (H3 fails). → oracle shows no gain; bottleneck is elsewhere; stop optimizing retrieval.

## 6. Arm family, multiplicity & the exploratory/confirmatory firewall

- **Phase-A (35 arms × 4 datasets = 140 dev cells) is EXPLORATORY** — dev-only mapping/screening (`phase_a_cells`),
  **no confirmatory claim**; its job is to rank arms per dimension to name Phase-B winners. Dev inference uses
  Holm/max-T within a dimension family but stays hypothesis-grade.
- **Confirmatory claims restricted to the pre-named Phase-B winners protocol on the LOCKED holdout** (n=60,
  group-disjoint, `LOCKED_TEST_SEED=611741209`, tag `grouplock-v2-20260711`) — **never touched in Phase-A**
  (Dwork reusable-holdout; split design §2). Winners frozen BEFORE the holdout is read.
- **Confirmatory family** = {`squtr`, `heysquad`} × { K pre-named winners (§10 item 4; recommend **K=2**) + the
  6 §5 controls }. Family-wise error via **Holm–Bonferroni (default) + max-T bootstrap step-down** (correlated
  tests: shared clusters across accents/renderings), both reported, disagreement flagged (stats §3.2).
- **Paired cluster bootstrap** on Δ (same cluster-resample indices for both arms), unit = cluster (squtr query /
  heysquad passage), 10 000 reps; output carries `n_clusters` + `bootstrap_unit` (stats §3.1). Item-level
  bootstrap forbidden for these two (both have real group structure).

## 7. Theory / effectiveness gate (two-tier, method-typed)

- **(T) well-posedness.** A **fixed, finite, one-shot** retrieve→inject→generate map (no iteration/online update
  — `assert_no_adaptive_logic`); no convergence theorem defined or required (Template §5). For a fixed MockConfig
  the delivered-passage set is deterministic in (similarity ranks, config), and `Δ_e2e` is a difference of two
  finite means → well-defined. Assumption to verify empirically: the CLEAN KB carries answer-relevant content
  (tested directly by H3 oracle).
- **(E) effectiveness** = the §1/§2 pre-registered empirical criterion on the locked holdout — measured, never proven.

## 8. SESOI + power sketch (n=60 locked test)

- **SESOI (owner-set, §10 item 2).** Default **0.05 absolute** on the primary metric (≈5 pts accuracy /
  containment-EM; nDCG@10 units if squtr retrieval-only) — drives both the go-threshold (point ≥ SESOI AND
  CI LB > 0) and the equivalence margin (Δ_eq = SESOI/2 = **0.025**).
- **Effective n = cluster count, not item count.** n_test=60 items map to **fewer clusters** (squtr ≈ distinct
  queries — clean+SNR renderings collapse into one each; heysquad ≈ distinct passages) — expect **~20–45
  clusters**, reported per cell as `n_clusters`; that count governs CI width.
- **Power sketch (rough, paired design).** The paired within-item contrast cancels item difficulty, so the
  relevant SD is the within-pair Δ-SD σ_Δ, not the between-item SD. 95% half-width ≈ 1.96·σ_Δ/√K; detecting
  SESOI=0.05 with LB>0 needs σ_Δ/√K ≲ 0.025 (σ_Δ ≲ 0.13 at K≈27, ≲ 0.17 at K≈45). **Honest caveat:** if
  empirical σ_Δ is larger (common for open QA), n=60 is under-powered for 0.05 → owner must accept a wider
  pivot zone (§9) or raise n_test before the lock (§10 item 6) — decided now, not discovered after the run.

## 9. Success / kill / pivot & stopping rules (pre-registered)

- **Go (H1 accepted):** point `Δ_e2e ≥ SESOI` AND 95% CI LB > 0 on `squtr`, AND same direction (CI LB > 0, no
  equivalence kill) on `heysquad`.
- **Kill:** either §5 equivalence kill fires → negative result.
- **Pivot:** CI crosses 0 but point ≥ 0 and no equivalence established → scope/re-power, do not claim (width
  driven by cluster count, §8).
- **Stopping rules.** Phase-A: run all 140 dev cells once (single-touch), no mid-sweep arm changes, no interim
  peeking that informs the holdout. Phase-B: **exactly one** read of the locked holdout after winners frozen —
  no re-draw, re-tune, or adaptive stopping; reading burns it (Dwork). Any later question needs a fresh locked
  draw with a new unused seed.

## 10. Owner sign-off checklist (Phase-B confirmatory run BLOCKED until all checked)

1. [ ] **Primary dataset = `squtr`**; **replication = `heysquad`** (confirm both, and confirm SQuAD-zh /
       vocalbench-knowledge stay exploratory-only).
2. [ ] **SESOI value** (default **0.05 absolute** on the primary metric — confirm or override per metric).
3. [ ] **Equivalence margins = SESOI/2 = 0.025**, TOST, 90% CI convention (confirm).
4. [ ] **Phase-B winner count K per dataset** (recommend **K = 2**) — set the number.
5. [ ] **`squtr` end-to-end reader metric** definition frozen (containment-EM recommended), or rule squtr
       retrieval-only → nDCG@10 primary.
6. [ ] **Power decision:** accept cluster-count-limited power at n_test=60 (pivot-zone widening allowed), or
       raise n_test before the lock.
7. [ ] **Locked-holdout params:** `LOCKED_TEST_SEED=611741209`, n_test=60 / n_dev=40, group-disjoint,
       tag `grouplock-v2-20260711` (already the 续13 default — confirm for these two datasets).
8. [ ] **Control-arm build gate:** no-retrieval / random-retrieval / oracle-retrieval / gold-transcript arms
       implemented + real-runtime E2E-green (G2) before the confirmatory run.

## 11. What CANNOT be claimed (scope fence)

- **No agent-convergence / "agentic system" grand claim** — this is a fixed-pipeline retrieval-causality study.
- **No W4 claims** (frozen-omni disentanglement / readout) — out of scope; shares no headline with W4 (G0 ②).
- **No oracle→deployable extrapolation** — oracle is a labeled ceiling; the deployable claim is own-ASR /
  audio-direct vs no/random only.
- **Transfer-study honesty.** If only the **ASR→text-cascade** arms win (text path, not audio-direct speech-keyed
  retrieval), report it as a **cascade/transfer** result — the speech-keyed claim requires the **audio-direct**
  arm itself to beat controls.
- **No unqualified metric** — exact definitions; no macro/corpus or zero-shot/transductive slippage (RI ledger).

## 12. AI tools & verification

Survey claims resolve to real sources (§3 registry). The confirmatory number is independently re-run from a
clean checkout by a different agent/person into the declared band, with a claim-specific code-review log
(ground-truth-derived score; no leakage; seed/env pinned; `reproduce:` runs clean; Template §4/§8). Adversarial
panel sign-off (statistician · reproducibility auditor · anti-gaming red-teamer) recorded before any grade upgrade.

---

*Append-only DRAFT. No numbers here are results; Stage-1 evidence stays hypothesis-grade. §10 signature required
before the Phase-A dev sweep (items 1–2, 5–7) and before the Phase-B confirmatory run (all items + G2). Not
committed by the drafting agent.*
