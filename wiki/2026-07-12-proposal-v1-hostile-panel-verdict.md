---
title: "提案 v1.1 敌对评审团裁决：RESTRUCTURE（5 FUNDAMENTAL + 12 MAJOR）"
date: 2026-07-12
stage: 1-problem-definition
status: "panel 裁决在案；提案 v2 重构待 owner 确认新 primary 问法"
reviews: 2026-07-12-research-proposal-RDU-frontend-knowledge-v1.md
---

# 提案 v1.1 敌对评审团裁决（四透镜 + 主席合议）

## 主席合议

**VERDICT: RESTRUCTURE.** Five independent FUNDAMENTALs converge on one fault — the primary question as posed is unpublishable (clean positive = foregone replication of ≥5 prior teams; clean negative = reads as a retriever bug — R4), and each of its three axes is separately broken: H2 is *forbidden* by the harness's no-adaptive-logic invariant, H5 injects its own answer, H3's estimand is winner's-cursed, and the co-primary threshold is self-contradictory. Not patchable in a revision pass; re-architect the primary, then re-review before signing.

**FUNDAMENTAL**
1. **Re-frame primary** (§1, §3). Elevate frozen-key sufficiency — "can a frozen omni model's own embeddings serve as a training-free retrieval key with zero trained projection?" (H1/H5a) — to primary; demote the 18-cell sweep to method-standardization. Pre-commit: if a projection must be trained, report as a *negative* on training-free, never swap silently.
2. **H2 trigger is forbidden AND uncited prior art** (§1, §3-H2, §4.2). Move the trigger to a separate two-pass pipeline outside the mock口径; cite FLARE/Self-RAG; reposition as "does active-retrieval transfer to frozen omni."
3. **H5 B-WER is answer-injection** (§3-H5, §4.1, §5②, App A). Make the deployable list an *outcome* of audio-key retrieval over a KB frozen before eval; the guaranteed-inclusion list becomes a non-deployable oracle arm; report retrieval recall separately; compute ≥15% conditioned on retrieval, not injection.
4. **Co-primary threshold contradictory, rule undefined** (§4.3, §1/§3-H4). Pick ONE scale; publish the (currently absent) per-dataset numeric SESOI table; declare co-primary success = intersection or union.
5. **H3 estimand ill-defined** (§3-H3). Replace "≥ any/max retrieval contrast" with a single pre-registered contrast (delivery main effect − key-modality main effect) + joint CI.

**MAJOR**
6. **Custodian not independent / commitment non-binding** (§4.4). Independent human co-signs; publish hash{script, eligible-ID set, seed rule} before drawing; seed from a public beacon; fresh session receives only the committed script.
7. **Firewall misses group leakage for 42 no-group sets** (§4.4, §5①). Commit pool group-disjoint from union(dev+old-test+65 exposed); drop no-group datasets from confirmatory or obtain a group key; re-run winner selection with the 11.2% overlap items removed.
8. **content_hash omits retrieval function** (§5③). Extend to embedder SHA+revision+quant+norm (assert key==query, fail-closed) + index params/top-k.
9. **Closed-book anchor subtracts non-comparable items** (§4.1). Redefine as within-item paired contrast (same audio, KB-provided vs KB-withheld) or drop "net"; enumerate it as a family member.
10. **H1 not runnable Week-1** (§10). Cross-modal routing is unimplemented and no KB persists on disk; Week-1 delivers own-ASR text-text arm + build/validate routing + re-key corpus. Report cascade ASR WER as covariate.
11. **Multiplicity family incomplete** (§4.3). One enumerated family per claim (H1–H5 + anchor); the H5 list-length sweep and closed-book anchor currently escape correction.
12. **Kills fire at the underpowered exploratory layer** (§8/§4.4). State no kill fires there; kills are confirmatory-only; exploratory output is ranking, not accept/reject.
13. **No interaction model for 2×3×3** (§4.2/§4.3). Pre-register it; select H4 winner on cell-level estimates; gate main-effect reads on interaction-CI width.
14. **H2 "等增益" accepts the null** (§3-H2). Declare a TOST margin on the gain difference; require the ≥30% call-reduction as a separate superiority test — both must pass.
15. **GPU budget ignores multi-pass arms** (§10, §6). Cost each arm by generation-pass count; measure one real cell before committing wall-clock.
16. **logit_bias/GBNF unbuilt + survey-predicted ~9%** (§7, App A). Label exploratory-only, not load-bearing for H5's 15%; note it needs new delivery code + token-realization enumerator.
17. **δ_corr both disclaimed and load-bearing** (§6/§7③). Either drop it from the theorem's constraints and cite ROVER/Fiscus as borrowed infra, or own it as a rescoring-adjacent contribution.

**Review-noise (dismissed):** R1-m1 (DL τ² with k=3–4) — valid but advisory; just report fixed-effect/per-dataset, not decision-bearing. R1-m2 (family double-count) — accounting detail folded into #11. R3-MINOR "工具递送 mislabel" — cosmetic; rename to "2-turn prompt delivery," no methodological impact. R3-MINOR "new scheduler" — implementation task, track as work not a design defect. R4-MINOR8 (accidental two-pass-gap occupancy) — subsumed by the #1 pivot.

---

## R1 统计与方法

# Hostile Review — Methodology & Statistics Lens

## FUNDAMENTAL

**F1. The co-primary threshold is internally contradictory; the primary decision rule is undefined (§4.3 vs §1/§3-H4).** §4.3 sets SESOI = 0.05 absolute "约 10-15% 相对." That equivalence holds only for baselines in ~0.33–0.50. The main场 datasets span very different baselines: at baseline 0.30, 0.05 abs = 16.7% rel; at 0.70, 0.05 abs = 7.1% rel. So "0.05 absolute ≈ 10-15% relative" is false as a cross-dataset invariant. Worse, the co-primary demands **both** "绝对 delta" (≥0.05) **and** "相对改善百分比" (§1/H4 ≥10%). On a high-baseline dataset these two bars conflict: +0.05 abs *passes* SESOI but *fails* the 10% relative bar; the study can "succeed" and "fail" its own primary simultaneously. Fix: pick ONE primary scale, declare per-dataset SESOI values numerically (frontmatter says these are pre-registered but they are absent), and state whether co-primary success = intersection (both) or union (either) — the union inflates α, the intersection loses power; neither is specified.

**F2. H3's estimand is not well-defined (§3-H3).** "递送增益 ≥ 检索段任何单维改进" = delivery gain ≥ **max** over retrieval contrasts. The maximum of noisy contrast estimates is upward-biased (winner's-curse), so the comparison bar auto-inflates and is not an estimable quantity. Also, in a 2×3×3 the retrieval dimension has only ONE factor (key modality); "any retrieval-dim improvement" is undefined — is it the key-modality main effect, or R@k retrieval quality? Fix: define a single pre-registered contrast (delivery main effect − key-modality main effect) with a joint CI; drop "any/max."

## MAJOR

**M1. The declared multiplicity family is incomplete (§4.3).** The family = "24 arms vs no-retrieval + 三维主效应." Excluded but inference-bearing: (a) **H5** three-段 vs full-list-stuffing on B-WER across 3 testbeds, with the **list-length sweep {2,5,10,50}** and true-word-ratio (附录A) — a multi-arm comparison with no declared family; (b) the **closed-book anchor** "RAG增益 − 闭卷增益 = 净外部知识贡献" (§4.1), a difference-of-differences headline with no test or family membership; (c) the **co-primary two endpoints** themselves. As written, only the exploratory 24-arm grid is corrected while every confirmatory-flavored side-claim escapes. Fix: enumerate ONE family per inferential claim (H1–H5 + anchor), with explicit contrast counts.

**M2. Kill criteria are applied at an underpowered exploratory layer (§8 #3 vs §4.3/§4.4).** §4.4 says all covered runs are exploratory ("只做方向分级"), yet kill #3 fires on "CI含0 (家族校正后)" and kill #1/#2 on TOST/CI outcomes — CI/equivalence decisions on dev data. With cluster bootstrap, effective N = **cluster count 20–45**, not 40; after Holm over ~28 contrasts, power to exclude 0 at a 0.05-abs effect is low. A non-significant exploratory CI then triggers a "转 limits 论文" kill — a **false-negative kill**. Fix: state explicitly that no kill fires at the exploratory layer; kills are confirmatory-only, and exploratory output is ranking, not accept/reject.

**M3. No interaction model declared for the 2×3×3 (§4.2/§4.3).** Main effects are marginally estimable, but H3/H4 (best combination, delivery≥retrieval) are meaningless if interactions dominate — and the priors *predict* interactions (uncertainty-trigger helps only under good delivery; audio-direct may help only under card). With 18 cells × n=40, interaction power is ~nil, so they'll be silently assumed negligible. Then the key-modality main effect averaged over flat delivery can be attenuated to null, wrongly downgrading H1. Fix: pre-register the interaction model, select the H4 winner on cell-level (not marginal) estimates, and gate main-effect interpretation on interaction-CI width.

**M4. H2's "等增益" has no equivalence margin (§3-H2, §4.3).** TOST margin=SESOI/2 is declared only for H4's random control. "在等增益下 ≥30% fewer calls" and "恒检索不显著优于触发" both **accept the null** from non-significant tests (absence-of-evidence fallacy). Fix: declare a TOST margin on the gain difference and require the ≥30% reduction as a separate superiority test; both must pass.

## MINOR

- **m1.** Cross-dataset DerSimonian-Laird pooling with k=3–4 datasets gives an unreliable τ²; random-effects CIs are anticonservative. Prefer fixed-effect or report per-dataset only.
- **m2.** "24 arms vs no-retrieval" double-counts no-retrieval (23 contrasts); the family arithmetic (23 + 5 main-effect contrasts = 28/dataset × 4) is never stated. DL pooling is aggregation, not multiplicity control across the 4 per-dataset families.
- **m3.** §4.3 promises SESOI "按各集基线换算并预注册具体值" but no numeric table exists — unsignable until populated.

---

## R2 边界与托管

I have enough to write a targeted hostile review. Findings below, on the BOUNDARY / CUSTODY / INTEGRITY lens.

---

**FUNDAMENTAL — H5's headline metric is answer-injection by construction (§3 H5, §4.1, §5②, Appendix A.4/§5).** B‑WER is scored *only on words in the bias list*, and the bias list for utterance *u* is built as `{rare words/entities in u's own reference} ∪ {N distractors}` with a pre‑registered *true‑word ratio*. That guarantees the reference entity is present for a set fraction of items — the experimenter injects the answer, then measures how well the model copies it. This is the C‑M3/C‑T7 failure class (ledger: `invalid`, "reading the answer off a smuggled‑in transcript"). The proposal never pins list membership to information available *before* the utterance is seen; the "true+distractor" convention derives the true word *from the gold transcript*. Half‑utterance‑absent + U‑WER penalties mitigate blind copying but do not fix the estimand. **Fix:** make the deployable H5 arm's list an *outcome* of audio‑key retrieval over a KB whose membership is frozen before eval; true‑entity presence must be recorded, never guaranteed. The guaranteed‑inclusion list becomes an oracle arm, permanently non‑deployable (like gold‑transcript). Report retrieval recall separately; compute the ≥15% target conditioned on retrieval, not on injection.

**MAJOR — Custodian is not independent and the commitment is not binding (§4.4).** (a) `custodian = owner 本人` violates Gate RI‑0/RI‑4, which demanded a custodian *not involved in design/running*; the owner signs the prereg (§11) — same party cannot draw the blinded test. (b) A "fresh AI session" has no agency; it deterministically executes the coordinator's prompt+seed. Blindness comes from commit‑then‑draw + a non‑grindable seed, not session freshness — as written the coordinator can draw many candidate sets and commit a favorable one (commitment‑after‑observation). **Fix:** an independent human co‑signs the draw; publish `hash{sampling script, post‑exclusion eligible‑group‑ID set, seed rule}` *before* drawing; derive the seed from a public future beacon; the fresh session receives only the committed script/pool; drawn IDs must be third‑party recomputable from revealed salt+seed. Commit the instruction text too.

**MAJOR — content_hash omits the retrieval function (§5③).** `content_hash = values+keys+ids+code` fixes stored vectors but not the *embedder weights/revision/quantization/pooling* (key‑ and query‑side) nor the *index type/metric/normalization/top‑k*. This is exactly C‑PHASEA P0‑4: "query‑embedder auto‑fallback silently swaps embedding spaces" — a swap reproduces the bug while content_hash still "matches." **Fix:** extend the hash to embedder SHA+revision+quant+norm config (assert key==query side, fail‑closed) and the index build params/top‑k; stamp per‑result index hash.

**MAJOR — Closed‑book anchor subtracts across non‑comparable items (§4.1).** "RAG‑gain − closed‑book‑gain = net external‑knowledge contribution" measures RAG‑gain on squtr/heysquad but closed‑book‑gain on a *different* dataset (vocalbench‑knowledge, "无 KB"). Cross‑dataset subtraction is confounded by difficulty/base‑rate/entity distribution — it is not a net contribution. (Also: vocalbench‑knowledge's KB was the *question's own text*, C‑PHASEA P0‑1.) **Fix:** define the anchor as a within‑item paired contrast — same audio/questions, KB‑provided vs KB‑withheld — else drop the "net" framing.

**MAJOR — Firewall catches ID overlap, not group leakage, for the 42 no‑group sets (§4.4, §5①).** Winners are selected on exposed‑dev‑like slices with 11.2% old‑test overlap; the fresh TEST is drawn from the same corpora. For 42/65 item‑level‑fallback datasets, group‑disjoint is impossible, so confirmatory items can be same‑speaker/same‑article near‑duplicates of the dev cells that drove selection — reusable‑holdout contamination the firewall misses. **Fix:** commit the eligible pool as group‑disjoint from the *union* of dev+old‑test+65 exposed sets; for no‑group datasets obtain a real group key or drop from confirmatory (Gate RI‑4). Also re‑run winner selection with the 11.2% overlap items removed.

**MINOR — own‑ASR cascade is boundary‑clean but confounds H1 (§4.2, H1).** The transcript is deployment‑realizable (no leak), but audio‑direct may "win" only because cascade ASR degrades under noise/accent, not because omni embeddings activate. **Fix:** report cascade ASR WER as covariate; both arms must retrieve over the identical frozen index.

---

## R3 可行性与工程

Findings below. I read the proposal, the RDU analysis, both surveys, `claim_ledger.yaml`, and verified against the code (`phase_a_cells.py`, `run_mock.py`, `kb_batch_build.py`, `kb_embed.py`) and the on-disk data root (E:).

**FUNDAMENTAL — the "发现/trigger" axis (H2) cannot exist in the harness as built.** The primary design is 2 key-modality × 3 trigger × 3 delivery (§1, §3-H2). But `run_mock.MockConfig` has six dimensions and *none* is a trigger; and the module is "STRICTLY NO ADAPTIVE LOGIC … no confidence gating, no per-item branching on the model's own output" (`run_mock.py` docstring + `assert_no_adaptive_logic`). Uncertainty-triggered retrieval is, by definition, per-item branching on the model's own logprob/entropy. So a full third of the primary factorial is not merely unimplemented — it is affirmatively forbidden by the harness's core invariant. Fix: specify the trigger arm as a separate two-pass pipeline outside the "mock 口径", and re-scope which harness runs it; do not present H2 as runnable in the current machinery.

**MAJOR-1 — H1's audio-direct arm depends on unimplemented cross-modal routing.** `kb_batch_build.py:188` states the audio-query→text-keyed-corpus case is "**NOT yet implemented — a known follow-up**"; non-omni embedders are recorded `ARM-BLOCKED-cross-modal` (lines 151-241). squtr's corpus is text-keyed (built for the own-ASR *text-text* arm only, line 191-192). Moreover **no KB source is persisted on disk at all** — there is no `knowledge_base/` directory and no `values.jsonl` under the data root; consistent with `C-PHASEA: invalid`. H1 is the flagship's primary retrieval comparison; it cannot run Week-1 until routing is built and the corpus is re-keyed. Fix: Week-1 delivers "own-ASR text-text arm + build/validate cross-modal routing," not the H1 head-to-head.

**MAJOR-2 — GPU budget ignores multi-pass arms and rests on an unmeasured constant.** §10's "~130 cells / ~1.5 GPU days" traces to `phase_a_cells.GEN_TIME_S=3.0s`, explicitly "NOT independently measured on this box (no cell has been executed yet)"; `_repro/step2_mock/` is empty. That constant assumes **one** generation pass/item. Own-ASR (`_asr_transcribe`), HyDE, and the H2 trigger each add a full extra pass (~2×), yet §6 budgets only an *offline CPU* threshold calibration, never the online first-pass cost. Fix: cost each arm by generation-pass count, re-derive the budget, and measure one real cell before committing a wall-clock.

**MAJOR-3 — H5 testbeds are half-present; the parts that make them testbeds are absent.** Audio is on disk (aishell-1, librispeech, slurp) but the annotation artifacts are not: `is21_deep_bias` bias lists (survey flags GitHub fetch blocked in this env) and AISHELL-NER labels must be acquired, B-WER scoring and oracle-list→retrieval alignment are unwritten, and the proposal itself freezes H5 only "附录 A 调研裁定后." Bundling acquisition + alignment + routing + G2-L3 into Week-1 is the 2× optimism. Fix: give H5 testbed build its own week, gated on the Appendix-A adjudication.

**MAJOR-4 — logit_bias/GBNF arms are unbuilt and, per your own survey, unfit.** `DELIVERY_MODES` has no logit_bias or grammar mode — A-inj-logitbias/A-inj-gbnf have zero code path. For Chinese entities (AISHELL-NER) the survey rules llama.cpp `logit_bias` a non-sequence-aware bag-of-subword, "surface-form fragile" (HB-8), so multi-token Chinese entities can't be reliably boosted; GBNF is hard-constraint-only (kills open transcription). Appendix-A §5 already predicts ~9% (below the 10% bar). Fix: label these exploratory-only, not load-bearing for H5's 15%; note they need new delivery code plus a token-realization enumerator.

**MINOR — "2-turn 工具递送" is mislabeled.** `_two_turn_messages`/`_gen_llamacpp_messages` send prefabricated turns in **one** generation call (t10 artifact: "2-turn tool-*style* injection"); there is no model-emitted tool call, no execute-and-feed-back round-trip. Good news for cost (~1×, no tool infra) but the "工具" framing overstates the mechanism. Rename to "2-turn prompt delivery."

**MINOR — new scheduler needed.** `phase_a_cells.py` is a one-factor-at-a-time marginal scan (35 arms), not the 2×3×3 crossing; a full-factorial scheduler is uncounted Week-1 work.

Net: Week-1 as written (G2-L3 + routing + H5 testbeds + trigger + 18-combo scheduler) is optimistic by ~2×; H1 and H2 are the load-bearing risks.

---

## R4 定位与先行研究

# Hostile Review — Lens: Positioning, Novelty & Prior Art

**FUNDAMENTAL-1 — Neither outcome of the primary question is a publishable surprise.** §1's primary = "which of 2×3×3=18 (key-modality × trigger × delivery) combinations beats no-retrieval by ≥10%." Stripped of defensive scaffolding this is "does adaptive RAG + good prompt formatting help a frozen omni model on spoken QA?" A clean *positive* is a foregone conclusion — the team's own directional §2 already has card-delivery +34.6% and the hotword survey rates the retrieve-then-inject hypothesis "STRONGLY SUPPORTED by ≥5 teams" on the *same* model family (Locate-and-Focus is literally on Qwen2-Audio, the direct predecessor). A clean *negative* would contradict both the team's directional data and 5 prior teams — read as a retriever bug, not a finding. **Fix:** demote the 18-cell sweep to method-standardization and elevate the one genuinely open sub-question (see FUND-2) to primary.

**FUNDAMENTAL-2 — The only real novelty is the element prior art predicts fails, and claiming it as success breaks the frame.** The sole differentiator vs BR-ASR/RECAST/Hotword-RL is "frozen-omni-embedding-as-key vs their *trained* retrievers." But the hotword survey's own HB-26 says off-the-shelf keys are dead (CLAP R@1≈0.1), all winners are purpose-trained, and the sole training-free analogue (M2R-Whisper) needs logit access you lack — so the proposal itself flags this as "an aggressive bet" and offers "a thin retrieval-projection training step" as backup. That backup *is training* — it voids "weight-frozen." **This is the publishable kernel if isolated:** "can a frozen omni model's own embeddings serve as a training-free retrieval key with zero trained projection?" A clean answer *either way* (esp. negative) is a real contribution because it isolates training-free-ness as the variable. **Fix:** make H1/H5a (frozen-key sufficiency) the primary; pre-commit that if a projection must be trained, the result is reported as a *negative* on training-free retrieval, not swapped in silently.

**MAJOR-3 — H1 is already answered in the surveyed literature.** Rescoring/hotword survey §4 (键模态谱) ranks audio-direct/cross-modal keys as "best fit, best results… avoid transcription-bootstrap failure," while BR-ASR's *text* key (TextualBias) is the actual winner (OOV-robust, fewer homophone hits). So the field already gives a differentiated answer, and it *undercuts the flagship* ("omni-embedding activation"), since it favors trained/text keys. The proposal frames H1 as open. **Fix:** cite this prior art in §3, and reframe H1 as *confirmatory replication under the training-free constraint*, not discovery.

**MAJOR-4 — Uncertainty-triggered retrieval (H2) is uncited prior art.** "Retrieve on per-sentence logprob/entropy threshold" is FLARE/Self-RAG (2023) — active/adaptive RAG — which neither survey covers and the proposal never cites. As written H2 replicates a known text-LLM method on audio. **Fix:** cite adaptive-RAG; position H2 as "does active-retrieval transfer to frozen omni," not novel.

**MAJOR-5 — δ_corr re-imports a rescoring research claim through the reward layer.** §6 disclaims output-rescoring ("信号不用于重排序研究主张"), yet §6/§7③ bake the δ_corr decorrelation constraint and "τ 可估" into the *load-bearing* theory track — and the rescoring survey §6.4/C19 explicitly names "δ_corr omni verifier > logprob" as *the only new research content* and an OPEN question with ROVER/Fiscus as prior art. You cannot both disclaim and make it load-bearing. **Fix:** either treat the reward layer as borrowed off-the-shelf infrastructure (drop δ_corr from the theorem's load-bearing constraints, cite ROVER) or own it as a rescoring-adjacent contribution and defend against 28-year-old prior art.

**MAJOR-6 — The ≥10%/≥15% bars are under-justified and non-discriminating.** §4.3 back-derives 10% from an asserted 0.05-absolute SESOI (no deployment/decision-theoretic basis), and a single *relative* bar across heterogeneous baselines is ill-defined. Survey §7 shows deployable prompt-injection yields 30–60% relative (15% trivially cleared → uninformative) while the native logit_bias lever yields ~9% (below the bar). **Fix:** set SESOI per-dataset from deployment cost, and per-mechanism, not one global 10%.

**MINOR-7 — logit_bias/GBNF white space (the survey's cleanest novelty) is an API affordance, and the proposal's own §7/appendix-A predicts ~9% (sub-bar).** Keep it, but position as engineering exploration, not a scientific pillar.

**MINOR-8 — The proposal accidentally occupies, then disclaims, the genuine "training-free two-pass on omni's own N-best" gap (rescoring C9/§4.2).** §6's self-logprob trigger *is* that cell. You do the novel act but leave it uncredited while headlining replications.

**Verdict.** As currently primary, **NO** — a top venue would not consider H1–H4 publishable answered cleanly in *either* direction (positive = expected replication; negative = suspected bug). The proposal over-fits to reviewer appeasement (8 kill criteria, every P0 mapped) at the cost of ambition. **A reframed primary — "can a frozen omni model's embeddings work as a training-free retrieval key with no trained projection?" (isolating training-free-ness) — IS publishable answered either way, including negatively.** Recommend that pivot before signing.

---

