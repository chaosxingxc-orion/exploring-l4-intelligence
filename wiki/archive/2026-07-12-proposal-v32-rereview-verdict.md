---
title: "提案 v3.2 复核裁决：REVISE-THEN-SIGN（B1-B4 + M1-M4，4 个 owner 决策位）"
date: 2026-07-12
stage: 1-problem-definition
reviews: 2026-07-12-research-proposal-omni-agentic-frontend-FULL.md
---

# v3.2 复核评审团裁决

## 主席合议

# CHAIR CONSOLIDATION — v3.2 Re-Review

**VERDICT: REVISE-THEN-SIGN.** v1 dispositions are genuinely discharged (R1: woven into §1–§11, not parked). No panelist demands RESTRUCTURE. Every surviving fundamental lives in the six newly-added walkthrough elements (§5.6 eligibility, §4.2 m=3 trigger, §9 ≤5 rounds) and is closable by pre-registration edits plus a bounded owner-decision set — no second panel needed.

**Ranked, deduped (must-fix before signature):**

**B1 — Iteration multiplicity × burn-firewall × pool supply** (merges R2 MAJ-3 + R4 FUND-1). ≤5 confirmatory rounds at α=0.05 each ⇒ FWER ≈23%; no alpha-spending; the burn-once firewall needs 5 disjoint draws the pool is never sized for; M5→M2 back-edge undrawn; attribution reads the burned test. Fix: alpha-spending across looks; M5→M2 back-edge drawn; per-round append-only prereg + fresh custodian/owner sign; attribution restricted to dev. *Editor for spec; OWNER must confirm holdout supply feasibility.*

**B2 — Eligibility rule §5.6②** (merges R2 FUND-1 + R2 MAJ-4 + R4 MAJOR-3). Dev-noise-inflated headroom admits datasets (winner's curse) AND shrinks the Holm denominator (double benefit); "2×SESOI" is unit-mismatched to headroom's scale; overlaps kill #3. Fix: judge on a third split disjoint from selection-dev and confirmatory; gate on headroom **CI-lower ≥ 2×SESOI in error-reduction units**; pre-register a fixed MAX family size, Holm at that size regardless of drops; restate kill #3 as dev→confirmatory divergence only. *Editor.*

**B3 — S3 discovery trigger** (merges R2 FUND-2 + R3 m-1 + R1 F2). m=3 self-consistency is near-binary/degenerate (τ* ≈ coin-flip); "agreement" undefined for span/WER/ASR; first-pass temp unspecified (greedy⇒degenerate); harness-separation asserted, "过 assert_no_adaptive_logic" incoherent. Fix: pre-register answer-equivalence per K-type; a distinct first-pass temp>0; scope the invariant to the mock + specify the separate S3 runner contract. *Editor for spec; OWNER must justify m (or raise it) and confirm S3 stays in-scope.*

**B4 — S4 retrieval-miss self-grading** (R1 F3). A true entity retrieval MISSED must count as a B-WER **error**, never excluded; B-WER reference-anchored, retrieval-conditioned only for the bias set. *Editor.*

**Major (editor, before sign):**
**M1** — H5's 15% rests solely on the unverified retrieval-short-list prompt (R1 M16 + R3 F2): gate on D6 first-cell + pre-commit fallback. *OWNER sets fallback.*
**M2** — Supersession tie-breaker resurrects the 续18-killed white-box layer; v2.1 frontmatter stale (R4 MAJOR-2): amend to "§0 as modified by 续16–19." *Editor.*
**M3** — Commit the 11.2%-overlap winner re-selection to M2 (R1 M7). *Editor.*
**M4** — Un-ledgered 24%/0.70, −0.134 (INVALID C-T7), 2-turn numbers applied inconsistently (R4 MINOR-5): mint directional IDs or downgrade; apply flag uniformly. *Editor + OWNER provenance.*

**Minor (batch, editor):** attach pass/fail thresholds to M2/M4 gates or label non-gating (R2 MIN-5); eligibility one-way + untracked survey/date promises → docs ticket (R2 MIN-6 / R4 MINOR-6); "合并"=pooled not max (R1 §5.6#7); stale §0 banner (R4 MINOR-4).

**Dismissed as scope-error:** R3's F1/F2/F3 framed as sign-blockers — a Stage-1 pre-registration is signed *before* M1 goes green; unbuilt cross-modal routing / S4 assets / two-pass harness ARE the M1 workload, not proposal defects. Their only protocol residue folds into B3/M1. Record R3's "M1 = several engineering-weeks, not one gate-check away" as a schedule note, not a sign gate.

**Sign gate:** B1–B4 + M1–M4 resolved. Editor closes all except four tagged OWNER decisions — pool supply, m-value, 15% fallback, ledger provenance.

---

## R1 处置审计

## Disposition Audit — v3.2 vs v1 panel (5 FUND + 12 MAJOR)

**Overall:** Dispositions are overwhelmingly GENUINE — woven into §1–§11 body, not parked in the §12 map. Two residuals rise to new findings.

### Five fundamentals (spot-checked hardest)

**F1 (primary reframe) — FIXED (via owner overrule).** §3.1 explicitly *rejects* the panel's "elevate frozen-key" fix and installs an effect-first system question; body is consistent throughout (§1.1–1.3, §2.5 "no stage-level novelty claimed," §3.2 H-sys, §9 iterate-on-fail, §3.3 demotes frozen-key to S1). Not cosmetic. Residual (accepted-risk, not defect): a hostile venue can still press whether an *expected-positive* effect claim is publishable; owner has signed for that risk.

**F2 (trigger outside mock口径) — PARTIAL.** §2.3/§3.3/§4.1 place S3 as an independent two-pass pipeline, cite FLARE/Self-RAG, and (key move) switch the first-pass signal from logprob to output-side m=3 self-consistency (§4.2, §7) — this genuinely removes the `assert_no_adaptive_logic` violation. But the separation is asserted, not operationally built: D5 harness is unbuilt (§11 M1) and the phrase "过 assert_no_adaptive_logic" is incoherent as written (a branch-on-output pipeline *is* adaptive). Fix: state that the invariant scopes the mock harness only and S3 runs in a *distinct* runner; specify that runner's contract.

**F3 (S4 retrieval-outcome lists) — PARTIAL.** Answer-injection is genuinely killed: §5.4 makes the deployable list an audio-key retrieval *outcome*, freezes the KB "eval 之前" into content_hash (§6.2), demotes guaranteed-inclusion to a permanent non-deployable oracle arm, and reports recall/homophone-precision separately (H5a). Gap: retrieval-**miss** accounting is under-specified. "B-WER 以检索产出为条件计算" is ambiguous — if a true reference entity that retrieval *missed* is excluded from B-WER, you have re-created a self-grading leak (only scoring what you retrieved makes recall failures invisible in the headline metric). Fix: pin that a missed true entity counts as a B-WER **error** (penalty), never excluded; make B-WER reference-anchored, retrieval-conditioned only for the *bias set*, not the *scored set*.

**F4 (single scale) — FIXED.** §5.6 collapses to one scale (relative error-rate reduction ≥10%); §3.2 explicitly drops the absolute-AND-relative double gate; per-dataset SESOI numeric table present; the old "0.05 abs ≈ 10–15% rel" cross-dataset invariant is killed; co-primary contradiction resolved by splitting into H-sys-a (go/no-go) vs H-sys-b (separately adjudicated, cannot kill -a). No residual dual-scale contradiction — SESOI is *derived from* 10%-relative, so §3.2's "≥10% 且 CI 下界越 SESOI" is single-scale.

**F5 (S2 single contrast) — FIXED (minor wording).** §3.3/§5.6#7 = delivery main effect − key-modality main effect, joint CI, family=1; winner's-curse "≥ any dimension" gone. Minor: "card+2轮 合并最优 vs flat" — clarify "合并" = pooled arm, not max(card,2-turn), else winner's-curse re-enters.

### Twelve MAJOR — verdicts

FIXED, genuine body content: **M6** §5.7 (indep co-sign+beacon+hash-before-draw); **M8** §6.2 (embedder SHA+key==query fail-closed); **M9** §3.2/§5.1 (within-item); **M10** §11 (M1 gate); **M11** §5.6 (full enumeration; note "provisional pending M2 re-enum" but discipline intact); **M12** §5.7/§9 (confirmatory-only kills); **M13** §5.6 (interaction pre-reg, cell-level); **M14** §5.6#8/#9 (dual-gate TOST+superiority); **M15** §5.5 (per-pass, upgraded to m+1); **M17** §7/§8 (δ_corr→borrowed infra, out of theorem, recall-floor substituted).

**M7 — PARTIAL:** §5.7 makes confirmatory pool group-disjoint, but the panel's "re-run winner selection with 11.2% overlap removed" is not explicitly committed. Add it to M2.

**M16 — PARTIAL (new risk):** arms removed (续18) so no longer load-bearing — but H5's 15% now rests *solely* on unverified retrieval-short-list prompt (§10 ⚠, §5.4). Honestly flagged, un-derisked. Fix: gate 15% on D6 first-cell measurement before signing.

### New findings
- **MAJOR** (§5.4): F3 retrieval-miss B-WER self-grading — see fix above.
- **MAJOR** (§10/§5.4): M16 15%-target now unbacked — pre-commit fallback if D6 misses.
- **MINOR** (§2.3/§11): F2 harness-separation unbuilt/mis-worded.
- **MINOR** (§5.6#7): "合并最优" ambiguity.

No item is COSMETIC-only.

---

## R2 新元素攻击

# Hostile Re-Review v3.2 — NEW-ELEMENT METHODOLOGY ATTACK

Scope: the six walkthrough additions only. I read the FULL proposal §3.2/§5.6/§9/§11, the v1 verdict, and cross-checked ordering against §5.5/§11-M2.

## FUNDAMENTAL

**FUND-1 — Eligibility rule is a dataset-level winner's curse that also loosens Holm (§5.6, condition ②).** Credit where due: the ordering IS specified — §11-M2 runs 全臂族 dev (which includes the `oracle-retrieval` control, §5.5) *before* 资格规则判定, and membership is mechanical given the pre-registered 0.85 / 2×SESOI thresholds. But two structural faults survive. (a) Condition ② screens on `oracle−bare-core` headroom measured at dev n≈40 (heysquad ci95 [0.10,0.35]) from the **same corpora** that feed confirmatory (§5.7 pool is group-disjoint but not corpus-disjoint). Datasets admitted because dev-noise inflated their headroom regress on the fresh holdout → inflated confirmatory pass rate. (b) Dropping datasets shrinks the Holm/max-T denominator (§5.6 admits "家族规模可能小于 15"), so the *same* screen that removes hard datasets **also weakens the correction on survivors** — a double benefit to passing. There is no multiplicity or CI treatment of the eligibility decisions themselves, and 2× is asserted with no decision-theoretic basis. *Fix:* judge eligibility on a third split disjoint from both selection-dev and confirmatory; gate on headroom **CI-lower ≥ 2×SESOI** (not point estimate); pre-register a fixed MAX family size and Holm-correct at that size regardless of drops.

**FUND-2 — m=3 self-consistency trigger is a degenerate signal (§4.2, §5.5, §7, §3.3-S3).** With m=3 the agreement rate lives in {1/3, 2/3, 1} — 0 is unreachable (the modal answer always has ≥1 vote), so **three usable values, one meaningful threshold** (trigger iff not-all-agree). The §7 Spearman calibration of signal→oracle-gain is then a 3-point curve with massive ties; τ* selection is a coin-flip. Worse, "agreement" is undefined for span/WER/ASR outputs — temperature sampling makes exact-match agreement ≈0, so the trigger fires on every item and S3's ≥30% call-reduction gate (family #9) is unreachable by construction. The entire discovery axis rests on this. *Fix:* pre-register answer-equivalence per K-type; power-justify m (report trigger ROC on dev); m=3 buys 3× first-pass cost (§5.5) for near-binary resolution — justify vs larger m.

## MAJOR

**MAJ-3 — ≤5 rounds = a 5-look sequential trial with no alpha-spending (§9 rule 2, §13-slot7).** Within-round Holm ≠ cross-round control; five fresh confirmatory draws each at α=0.05 inflate FWER to ~1−0.95⁵ ≈ 23%. Two compounding gaps: (i) **holdout supply** — each round is 单次消费/读取即 burn (§3.2), so 5 group-disjoint burns draw from a pool already stripped of the 42 no-group datasets (§5.7/M7); no supply arithmetic is shown and it is likely infeasible. (ii) Attribution ("分解归因瓶颈段") reads the burned confirmatory result, so round k's revision is adaptive to confirmatory outcomes. *Fix:* alpha-spending/group-sequential budget across the ≤5 looks; prove holdout N supports 5 draws; restrict attribution to dev; per-round prereg append-only, committed before the next draw.

**MAJ-4 — SESOI-scale incoherence inside the eligibility rule (§5.6).** "2×SESOI" is in error-rate-*absolute* units, but headroom = `oracle−bare-core` has an unstated scale (accuracy-gain vs error-reduction). If headroom is accuracy-gain and SESOI is error-absolute the 2× bar is unit-mismatched. *Fix:* define headroom in the same error-reduction scale as SESOI; show the equivalence per dataset in the §5.6 table.

## MINOR

**MIN-5 — DAG gate measurability uneven (§11).** Eligibility and the 1.5× budget-interrupt are numeric; but M4's cross-core portability smoke (D17, "1–2 集轻验作可迁移性证据") and M2's three-段 attribution carry **no pass/fail threshold** — a null smoke does not gate anything. Label them non-gating deliverables or attach a binary criterion.

**MIN-6 — Family re-enumeration:** the "重枚举 ≠ 事后收窄" claim (§5.6) holds only if the removed rows never re-enter; state that eligibility is one-way and re-computable by a third party from the frozen dev artifacts.

---

## R3 工程可行性

Assessment complete. Findings below — engineering-feasibility lens on v3.2 as specified, checked against W1 HEAD `e30af76`.

---

**FUNDAMENTAL**

**F1 — Cross-modal routing (audio-query→text-keyed corpus) is NOT implemented; an M1 exit criterion is unmet and the flagship depends on it.** `scripts/knowledge/kb_retrieve.py` docstring (Known follow-up, RI item 9) states plainly: `_query_embedder` picks the query embedder from `key_modality` alone and "would currently route such a source's queries through its text branch regardless of the caller's actual query modality… Not fixed in this pass." So every audio-key arm — S1 omni-own flagship, H1 audio-direct, §4.3 GLAP/nemotron keys — cannot query the text-keyed corpus today. §11 M1 lists this as a gate; §10 risk row rates it high×high. Fix: wire `kb_embed.embed_audio(queries, embedder=manifest.embedder_token)` against text-keyed omni sources + held-out validation. Until then only the own-ASR text-text arm (D1) runs; the audio-key flagship cannot reach M2.

**F2 — S4 testbed assets are absent on disk and uncoded.** `is21_deep_bias`: not in `docs/datasets.lock.json`, no loader, not in E:\…\datasets. `AISHELL-NER`: not in lockfile, no NER loader (only `loaders/aishell_1.py`, ASR-only), NER annotations not on disk. No B-WER/B-CER scorer exists in `metrics.py`. All four D4 sub-deliverables are unbuilt. Critically, item-2's promotion of AISHELL-NER as the SOLE zh knowledge field once SQuAD-zh exits (§5.6/§2.6) rests on a dataset **not loadable today** — the zh-coverage claim is currently unsupported. Fix: derive is21 biasing lists (LibriSpeech present) + AISHELL-NER tags (aishell-1 present), write 2 loaders + a B-WER scorer. Multi-day, not a gate-check.

**F3 — No two-pass / active-retrieval code path exists, and the one pipeline structurally forbids it.** `run_mock.py` enforces `assert_no_adaptive_logic` as a strict runtime invariant banning conditional/gating/reward logic (lines 274–286, 1403). D5's harness (multi-sample first pass → self-consistency → conditional retrieval → second pass) is entirely unbuilt; `t10_proto_agentic_2turn.py` is S2 delivery, not S3 discovery. Fix: build a separate out-of-mock harness — net-new scope.

**MAJOR**

**M-a — oracle-retrieval is not runnable on the eligibility candidates, yet it gates the whole family table.** §5.6 condition ② (headroom = oracle-retrieval − bare-core, dev-measured) must be evaluated at M2 for the "待定" datasets. But: heysquad KB is only a 50-rec PoC slice (`kb_registry`: `heysquad_poc`, not the full key); SQuAD-zh "never persisted via kb_build"; SLURP buildable but unbuilt; squtr corpus built (fiqa, 310 docs) but audio-side blocked by F1. The eligibility gate deciding family membership is itself unbuilt — KB sources for 3 datasets must be constructed first.

**M-b — G2-L3 clean rebuild (M1 criterion) pending.** Only G2 layer-2 CPU prep landed (commit `13d06f3`); the layer-3 real-machine/GPU ref-config rebuild is not done, and §6.4 makes it a hard prereq for squtr producing any legal cell. Depends on resident llama-server GPU + F1.

**MINOR**

**m-1 — self-consistency arithmetic is consistent but the sampling regime is unspecified.** §5.5/§7 m+1 costs are internally coherent (untriggered m=3, triggered 4; 8 cells→24–32 passes ✓). However the m=3 first-pass agreement signal requires temp>0; the baseline (§5.2) is greedy temp 0.0, under which m samples are identical (agreement≡1, degenerate). Pre-register a distinct first-pass sampling temp.

**M1 readiness verdict:** Of 6 named M1 exit criteria, ~1 (own-ASR text-text, D1) is near-ready. Cross-modal routing (F1), S4 protocol (F2), two-pass harness (F3), G2-L3 (M-b) are unbuilt; D6 cost calibration cannot run until a real pipeline exists. This is not "one gate-check away" — realistic scope is several engineering weeks: 2 dataset acquisitions + 2 loaders + B-WER scorer + cross-modal bridge + new S3 harness + GPU L3 rebuild + KB builds for 3 datasets. **M1 is not imminently green.**

---

## R4 一致性与治理

COHERENCE & GOVERNANCE SWEEP — v3.2 (`2026-07-12-research-proposal-omni-agentic-frontend-FULL.md`). Read end-to-end against v1 verdict, Decision-Log 续15–19, claim_ledger.yaml, v2.1 skeleton. No files modified.

**FUNDAMENTAL**

1. **Iteration loop × burn-firewall × finite pool collide, unspecified (§9#2, §11 M5, §5.7, §13 slots 6/7).** §5.7 mandates "确证工件读取即 burn，不得二次探索," yet §9#2/M5 allow ≤5 confirmatory-failing rounds. Each round therefore needs a FRESH locked draw, disjoint from union(dev+old-test+65-exposed + every prior round's now-burned set). The proposal never (a) names the DAG re-entry node — §9#2 says "重新探索" (implies M2) but "修订组件" may force M1 routing rework, and no back-edge is drawn; (b) pre-sizes the pool for up to 5 disjoint draws; (c) provides per-round custodian co-sign + Phase-B — slot 6 signs the draw once, slot 3-of-M3 signs Phase-B once. Fix: draw the M5→M2 back-edge, pre-size the disjoint pool for ≤5 locked draws, require fresh custodian draw + owner Phase-B sign each round.

**MAJOR**

2. **Conflict-resolution clause is a self-contradicting supersession (frontmatter L6 vs L27; v2.1 §0⑤).** FULL both "supersedes: …-v2.md" (L6) and rules "两者若有出入，以 v2.1 §0 的 owner 裁定为准" (L27). But v2.1 §0⑤ still mandates the "白盒扩展层单独申报" that 续18 later KILLED — so literally applying "v2.1 §0 governs" resurrects the deleted layer. The tie-breaker predates 续18/19. Fix: amend to "v2.1 §0 as modified by 续16–19 / latest owner ruling"; update v2.1's status frontmatter (still reads pre-续18, "白盒扩展层单独申报" as live) to record §0⑤'s reversal.

3. **Eligibility ② and kill #3 overlap; boundary asserted not operationalized (§5.6 vs §9#3, §5.1 L216).** Both key on oracle-retrieval headroom: ② drops a set dev-time when headroom<2×SESOI; kill #3 exits when oracle "无增益" (≈0 ⊂ ②). §5.1 claims "独立、互不替代," but a zero-headroom set satisfies both, and since ② is judged dev-only pre-confirmatory, kill #3 is unreachable for any set that already passed ② — it is leftover. Fix: restate kill #3 as governing only dev→confirmatory headroom divergence, or fold into the eligibility rule. (Relatedly, slot 2 bundles threshold+SESOI table+eligibility rule under one signature — three distinct governance decisions; consider splitting.)

**MINOR**

4. **Stale/mis-versioned banner (§0 L20).** "本文所有『白盒扩展层』表述…待 v3.1 编辑清除" — cleanup is done (grep: 白盒扩展层 survives only inside cancellation notices L35/177) and this is v3.2. Reads as an open promise. Update to "已于 v3.1 清除."

5. **Un-ledgered numbers applied inconsistently vs verdict_vocabulary ("无 ledger ID = unverified").** §1.4 self-flags the 24%/0.70 keep-rate ("签署前须补 ledger ID"); §4.1 L173 repeats the same 24% WITHOUT the flag. gate−inject=−0.134 (§1.4 L66 "第一定律" + §8 recall-floor theorem motivator) is drawn from INVALID entry C-T7 and has no separate ledger ID, yet is un-flagged. "2-turn 0.175→0.35" (§1.4) is attributed to C-MINDS-V2 but that sub-result is absent from the C-MINDS-V2 ledger entry. Fix before signature: mint directional IDs (C-T7-GATE, C-KEEP, C-MINDS-2TURN) or downgrade to qualitative; apply the flag uniformly.

6. **Untracked promises (no D-ticket/M-gate).** §2.6 "两份 survey 顶部各加日期注记," the 2 survey-scoped NEEDS-DATE-CHECK verifications (arXiv:2604.12398 ID anomaly; HB-33 PDF), and §4.3 "两个记忆笔记级事实若需硬核验请另标" are all promised but absent from D1–D18. Attach to M1 or a docs-hygiene ticket.

Supersession chain otherwise coherent (v1 REJECT record is append-only-historical; family count 15 reconciles §3.2↔§5.6↔§3.3). Findings 1–3 block clean sign-off.

---

