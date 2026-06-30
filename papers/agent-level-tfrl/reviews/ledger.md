# Resolution / scope ledger — multi-round adversarial review

> The meta-chair consults this ledger to classify each round's findings as NEW vs already-resolved /
> already-scoped-with-teeth. A finding is "resolved" only when the paper / Lean / experiments changed in
> **substance** (or the claim was cut); "scoped" requires an explicit, falsifiable limitation in the text.

## Round 1 (fresh adversaries `wf_ad0f7863-32d`; chair verdict: major revision, 6 critical + 11 major)

The decisive structural finding — accepted, not rebutted — is that the original "single-model inert → agent
**recovers**" thesis was **not supported by the theorems** (`qstar_product` proves the isolated optimum equals
the monolithic optimum) and **contradicted by the paper's own data** (speaker ~chance; emotion fragile). The
whole paper was **reframed** around the honest, provable thesis: *gain is governed by reward spread, not model
class; isolation adds nothing structurally; agents help only by introducing non-degenerate verifiable rewards;
the paralinguistic flagship is the hard case where our own evidence is negative/fragile.* Title changed.

| Finding | Severity | Resolution (substance) |
|---|---|---|
| OSA2-RECOVERY-UNSUPPORTED | critical | **Reframed.** §5 now states `qstar_product` ⇒ isolated optimum = monolithic; isolation adds no enlargement; "recovery" is the empirical Conjecture 1. NEW Lean theorem `gain_pos_of_nonconstant` (non-degenerate block ⇒ strictly positive gain, sorry-free) makes "growing in k" non-vacuous. Title drops "Recovers". §7 speaker/emotion flatness flagged as a standing counterexample for paralinguistics. |
| OPA-DEVTEST-SELECTION-LEAK | critical | **Fixed by re-run.** New `pool_method_probe_paired.py`: dev-selected layer + paired-delta bootstrap + 5 seeds. Result: mean Δ=+0.037, paired CI excludes 0 in **2/5 seeds** (the +0.097 was the best seed under oracle test-selection). Anchor removed; honest fragility reported. Artifact: `_repro/emotion_pool_paired_v2.json`. |
| TWO-OMNI-NOVELTY-COLLAPSE | critical | **Reframed.** §7/§8 acknowledge the frozen omni content embedding is ~chance on speaker / weak on emotion, so it does no load-bearing paralinguistic retrieval; honestly repositioned as omni-policy + classic speech-encoder (ECAPA/SER) memory; joint-retrieval ablation proposed. |
| GATE-ABSENT-WHERE-CONTRIBUTION-LIVES | critical | **Scoped with teeth.** §8: the gate is genuinely verifiable only on content/intent; for the paralinguistic cross-session loop it degenerates to a self-consistency surrogate (Goodhart-prone) — said plainly, renamed, with a decoupling + periodic-calibration protocol. |
| NO-TRIVIAL-BASELINE | critical | **Fixed in plan (pre-registered).** §9 adds ECAPA+SER+dict as the PRIMARY baseline the agent must beat (paired CIs), a query-generalization split, a no-gold-label leakage control, and numeric DER/SER admission bands. |
| REPRO-DISCREPANCY-AND-ARTIFACTS | critical | **Partially fixed + scoped.** Emotion result now has a committed JSON + `reproduce:` command. The SLURP/MInDS baseline discrepancy vs the project's `docs/theory.md` is reconciled/disclosed (one baseline per task, selection rule stated, marked a second pipeline not re-run here); full artifact-commit for the Op-B numbers is an explicit Phase-0 deliverable (teethed limitation). |
| TITLE-CONCLUSION-OVERCLAIM | major | Resolved (title + conclusion reframed to mirror §5 hedges; OSA-3 demoted; "trichotomy"/"stability tax" dropped). |
| ASSUMPTION1-GTHETA-CONTRADICTION | major | Resolved: §5 splits verifiable rewards into label-derived (independent of g_θ: WER/exact-match) vs model-dependent (probe/retrieval — functions of g_θ); Goodhart-immunity restricted to the former. |
| MOTIVATION-WRONG-MODALITY | major | Resolved: §7 tables separated by channel; demonstrated high spread is content/intent only; paralinguistic recovery labelled conjectural/negative. |
| LOADBEARING-PREPRINT-CITES | major | **Verified (favourable).** jitrl2026 = ICML 2026 Spotlight (peer-reviewed), claim accurate; skillsbench2026 stat (+16.2pp, 16/84 neg) accurate (domain variance +4.5–+51.9pp noted). Bib annotated; over-cautious hedges removed. |
| LEAN-QUANTITATIVE-WRAPPERS | major | Resolved: appendix relabels the 3 quantitative results as "Lean-checked consumption of an external bound" (Hoeffding/Pinsker as hypotheses; the one documented sorry); NEW strict lemmas added sorry-free; `lake-manifest.json` committed. |
| SINGLE-SEED-MULTIPLICITY-FRAGILITY | major | Resolved for the emotion anchor (multi-seed + paired CI + FWER-aware dev-selection); other numbers relabeled/scoped; Op-B multi-seed re-run scoped to future. |
| SID-NOT-VERIFIABLE-UNDER-DER | major | Scoped: §8 adds the DER-contamination caveat; SID reported jointly with DER; "verifiable" only under oracle/single-speaker segments. |
| SPREAD-BETA-UNFALSIFIABLE | major | Resolved: deleted the unfalsifiable "bounded by spread²/(8β)" claims (no numeric spread/β); raw effects + MDE framing. |
| BENCHMARK-CONTROL-VALIDITY | major | Resolved in plan: listen-control on ASR transcripts (+ normalized) + positive control + topic balancing; spontaneous (non-acted) affect corpus; IAA-survival reporting. |
| OSA1-RANGE-NOT-VARIANCE | major | **Partially + scoped.** §5 remark added (range vs concentration; ceiling = min(spread, spread²/(8β)); vacuous as β→0; stop calling it "realized"). A Bernstein/variance bound *formalized in Lean* is explicit future work (the paper-level remark stands now). |
| OSA2-IDEALIZED-HYPOTHESES | major | **Scoped with teeth.** OSA-2/3b explicitly labelled "idealized separable-case"; transfer to real agents with shared context + scalar joint return disclaimed; a perturbation/coupling bound named as the single largest open theory-to-practice risk (future work). |

**Open / deferred (explicit, falsifiable future work — not hidden):** a Lean-formalized variance/Bernstein OSA-1
bound; a coupling/perturbation degradation bound for OSA-2 under block dependence; multi-seed re-runs and
committed artifacts for the Op-B content/intent numbers (Phase-0). These are stated as limitations in the paper.

## Round 2 (fresh panel `wf_be2e7d7e-7a1`; chair: major revision, NOT clean, 13 new major). Root cause: the
round-1 reframe was applied to the body but not propagated to the most-read sections. All 13 resolved in substance:

| Finding | Resolution |
|---|---|
| F1 KL-direction typo (appendix proof of `gain_pos_of_nonconstant` wrote `KL(q*‖q0)`) | **Fixed** — corrected to `β·KL(q0‖q*)` matching `F_sub_eq_beta_mul_kl`; appendix KL directions audited. |
| F2 front-matter desync (abstract/C1 keep "stability tax"; false "Pinsker discharged"; omit the sorry) | **Fixed** — abstract/C1 re-synced: two load-bearing results + a nonnegative rollout-deficit corollary; "Hoeffding discharged on paper, Pinsker + Beirami order-statistics consumed as hypotheses (latter = the one documented sorry)". |
| F3 "realized spread" retained vs §5 retraction | **Fixed** — "realized" deleted globally; thesis = reward *range* (+ variance to leading order); ceiling stated range-based. |
| F4 "agentic recovery" contradicts `qstar_product` | **Fixed** — language removed; content/intent gains labelled single-model high-spread; "does agentic decomposition add anything" stated untested. |
| F5 title "Not Model Class" undercut by the model-class-switch remedy | **Fixed** — retitled "…Not Search Effort or Agent Wrapping…"; scope sentence added that spread is model-induced. |
| F6 emotion reported by 2/5 vote-count, not across-seed CI | **Fixed by correct statistic** — across-seed mean +0.037, 95% t-CI **[−0.043, +0.116] spans 0 ⇒ NULL**; reported as "no significant emotion gain at the across-seed level"; "2/5" demoted to a footnote; "fragile"→"null". Artifact JSON updated. |
| F7 evidence-accumulation confound (more sessions = more audio) | **Fixed in plan** — fixed-audio-budget / evidence-matched control; classic baseline fed identical accumulated evidence; vs-empty-memory contrast demoted. |
| F8 tautological "0 regressions" rerank | **Fixed** — stated structural (improve-only selector), replaced with a per-item paired CI / removed robustness claim. |
| F9 provenance under-specified (SLURP/MInDS baselines, missing n/CI) | **Fixed** — selection rule + slice per pair; n for SLURP/URO; CI for MInDS +0.089 or removed; one canonical MInDS row. |
| F10 baseline update rule unpinned | **Fixed in plan** — pre-registered running-ECAPA-centroid + SER-decay + change-detection rule in the locked artifact. |
| F11 system has no mechanism to beat the baseline; Phase-2 pre-registers a null | **Reframed (substantive)** — system DEMOTED from "flagship worth building now" to a **speech-agent testbed / falsification harness**, with ONE concrete candidate winning mechanism (Bayesian multi-session speaker-evidence integration under channel variation single-enrollment ECAPA misses) + its isolating ablation. |
| F12 calibration safeguard reintroduces deployment human labels (vs label-free premise) | **Fixed** — calibration cost made explicit (labels per population/drift/new-speaker); no-calibration ablation added; "sibling extractor" replaced by a committed independent extractor + agreement-with-truth. |
| F13 negative over-generalized to the generative policy | **Scoped** — negative precisely scoped to one content bi-encoder's linear-probe geometry; explicitly does NOT bound the untested generative Operator-B policy or "frozen omni models" as a class. |
