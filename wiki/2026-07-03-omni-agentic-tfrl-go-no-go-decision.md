---
title: "Decision: NO-GO — omni agentic TFRL step-1 rationality campaign (agent-level question closed)"
date: 2026-07-03
recommended: NO-GO
owner_verdict: PENDING
freeze_anchor: b19bff2
prereg: wiki/2026-07-03-agentic-tfrl-step1-preregistration.md
null_hypothesis: "2026-07-02 deep-review NO-GO (papers/agent-level-tfrl/reviews/deep-review.md)"
campaign_runs: wf_a68f9164-b3c / wf_68e2556d-7a7 / this run
skeleton: "prereg §9.2 (B.2 NO-GO skeleton)"
---

# Decision: NO-GO — agent-level question closed

## 0. Role, provenance, and mechanical discipline

This document is compiled by the decision-document compiler under role separation (prereg §6.10): the compiler authored no lane defense and no criteria arguments. Prereg §2 is applied criterion by criterion with no new arguments. Every number below traces to a committed `_repro/` artifact or a campaign lane file; artifact summaries were re-read from disk during compilation (`_repro/m3_phase0_zero_support.json`, `_repro/m5_selector_dev.json`, `_repro/m5_selector_confirmatory.json`, `_repro/asr_bon_llamacpp_snr5.json`). Skeleton: Appendix B.2 of the prereg (NO-GO), as required by where the criteria land. Provenance note on lane inputs: the Phase-5 meta-chair struck all panel-time citations to "B3/B4/B5 memos" as unverifiable because those deliverables were not on disk at panel time; the B3/B4/B5 lane memos were subsequently produced in this run and are cited below as this run's lane inputs. Where a lane recommendation conflicts with a panel ruling (see U2), the panel ruling governs (safeguards 3 and 10).

## 1. Verdict summary — the two questions answered separately

**Question (i) — Part A: is single-model training-free RL on frozen omni speech models rational as a direction?**
**RATIONAL-AND-CONTINUING** (Part-A memo, `wiki/survey/2026-07-03-step1-part-a-memo.md`, verdict section). A1 holds: oracle best-of-N headroom on the frozen Qwen3-Omni-30B is real and independently recomputed — greedy WER 0.1183 → oracle@8 0.0765, reduction **+0.0418, 95% CI [0.0289, 0.0564]**, three disjoint gen-seed slices all positive (+0.0506/+0.0480/+0.0270) (`_repro/asr_bon_llamacpp_snr5.json`). The fresh confirmatory slice independently re-measured real oracle headroom: greedy 0.0772 → oracle@8 0.05342, +0.0238 (`_repro/m5_selector_confirmatory.json` summary.arms). Part-A's KILL condition (A1 replication failure AND best-selector null) did not fire. **Post-memo update the record must carry:** the Part-A memo's A2 "open-and-promising" pillar rested on the M5 confirmatory being "designed and unrun" (memo §A2); it has now run, and deployable label-free capture measured ~0% of the real headroom (MBR-vs-greedy −0.00003, CI [−0.00358, +0.00369]; realized_fraction −0.0008). Part A continues via **P-D condition-mapping** plus the named untried in-fence single-shot selector families (S6-residual per-token logprob; frozen-judge rescoring — Part-A memo §A2/§A3), with the honest floor that every deployable selector measured to date is null.

**Question (ii) — Part B: should we build the omni agentic system (skills/memory/routing over frozen models)?**
**NO-GO.** The 2026-07-02 verdict stands — reaffirmed by fresh pre-registered measurement, not by default. No mechanism lane survived its E-part; no pivot trigger fired; the panel sustained all six charges and all 24 argued objections. Part-A rationality is not GO-weight for question (ii) — conflating them is the category error the prereg's (i)/(ii) split exists to prevent.

## 2. Criteria scoring table (prereg §2, applied mechanically)

| Criterion | Frozen requirement | Measured outcome | Verdict | Evidence |
|---|---|---|---|---|
| **G1 (mechanism)** | ≥1 lane M1–M5 survives BOTH T-part (non-tautological formal statement) and E-part (pre-registered threshold, paired-bootstrap CI-LB > 0, no-agency control null) | M3: Phase-0 pooled entity-match **F = 0.38108** vs kill 0.01 (38× over), CI [0.24477, 0.51823], KILL = true, consistent across 4 seed blocks (0.36111/0.40278/0.38194/0.37847), 439/1152 matches, greedy alone contains the entity 38.9%. M5: confirmatory **delta_vs_mbr = 0.0, CI [0.0, 0.0]** vs threshold 0.015; sel_wer_8 = mbr_wer_8 = 0.07722 exactly; zero flips in 432 items; PASS(i) = PASS(ii) = false. M2/M4: design-only, E-parts scheduled post-GO → inconclusive = NO-GO; both blind refuters "likely-dies". M1 never opened (conditional on M4 residue). T-parts: "STATED, not proved," zero Lean lines (chair C1). | **FAIL** | `_repro/m3_phase0_zero_support.json` (commit 1b53b46); `_repro/m5_selector_confirmatory.json` (commit f8ec1d3) summary.verdict; M2/M4 lane files; chair C1 |
| **G2 (VoI > 0)** | A NAMED downstream decision that changes with the answer + pre-registered step-2 kill criteria | B4 names four decisions (D-1 selector build, D-2 WF-2 scope, D-3 corpus path, D-4 W4 queue) with behavioral proof — two resolved by measurement this week (M3 Phase-1 cancelled; V4 selector build killed) — and pre-registers step-2 kill criteria K1–K6. Panel ruling: **U2 STANDS** (defense's panel-time exhibit was a phantom citation, struck; the frozen V1\|0.05 selector was pre-proven inert — median required λ 60.5 vs frozen 0.05 — so the exact tie was predicted, zero information ex ante). | **SATISFIED-IN-FORM / MOOT** — cannot convert absent G1; panel: U2 stands | B4 lane memo §2, §3, §6 (this run); chair C3; `_repro/m5_selector_confirmatory.json` |
| **G3 (ingredients ≥2/3)** | Operator + corpus + theorem, ≥2 concretely satisfied | Operator: resolved (S2; llama.cpp best-of-N, `_repro/asr_bon_llamacpp_snr5.json`). Corpus: formally satisfiable via pseudo-session paths (built and exercised: `_repro/m3_phase0_selection.json`, `_repro/m5_confirmatory_slice_ids.json`) but measured hollow/dead on both exercised surfaces (≤3/144 actionable dev positions; 0 flips on the designed surface); real corpus r1 verified NOT MET (12 empty searches, D2 negative findings). Theorem: dead — both G1 candidates killed mechanically; r2 verified EMPTY (D1 negative findings). B3 three-ingredient substantive test: **no task family passes all three** (F1 a✓b✓c✗; F2 a✓b✗-hollow c✓; F3 0/3; F4a/b/c fail). Ambiguity resolves against GO (safeguard 1). | **FAIL** (substantive); lenient 2/3 reading cannot convert and is moot given G1 | B3 lane memo §§1–5, 7 (this run); D2/D1 negative findings; `_repro/m5_selector_dev.json` structural_null_diagnostic |
| **G4 (budget)** | Minimal build ≤3 person-weeks, single 24 GB RTX 5090, no licensing/consent blockers | All three minimal builds fit: GO-minimal ~1–1.5 pw; P-A ~1–2 pw; P-B tier-1 ~1.5–2.5 pw; runs demonstrated on the single GPU (confirmatory 25,988 s ≈ 7.2 h; Phase-0 1,886 s); licensing clean as scoped. Feasibility is nowhere the binding constraint — evidence is. | **PASS (non-binding)** | B5 lane memo §§1–3, 6 (this run) |
| **GO (conjunction)** | ALL of G1–G4 | G1 FAIL, G3 FAIL | **FAIL** | above |
| **GO-minimal** | Only-M5 pass AND shuffled-memory ablation load-bearing (shuffled loses ≥50% of gain) AND G2/G4 at reduced scope | M5 PASS = false; ablation moot: gain_sel = +0.00000, gain_shuf = +0.00000, retained = null, load_bearing_le_50pct = false | **FAIL** | `_repro/m5_selector_confirmatory.json` summary.ablation + summary.verdict |
| **NO-GO clause (a)** | B0 fails (no admissible delta) | Not met — all four mechanism lanes stated admissible axes (M3: a; M5: b; M2/M4: c); no lane closed at B0 | not invoked | lane files, B0 statements |
| **NO-GO clause (b)** | All lanes hit kill thresholds AND M5 ablation shows accumulation not load-bearing | Executed lanes both hit: M3 F = 0.38108 vs 0.01; M5 no-pass 0.0 vs ≥0.015. Unexecuted lanes (M2/M4 design-only; M1 unopened) are inconclusive → NO-GO by the frozen rule. Ablation: accumulation NOT load-bearing (gain 0.0/0.0). | **MET — via executed-lane kills + the inconclusive→NO-GO default for unexecuted lanes (M2/M4 design-only, M1 unopened; strict-all-lanes reading not claimed)** | artifacts above; prereg §2 |
| **NO-GO clause (c)** | 10-working-day timebox expiry | Decision reached on day 1 of the box | not reached | prereg header |
| **P-A trigger** | M5 E-part ≥0.015 vs MBR, CI-LB > 0, fresh slice, ablation negative | Measured 0.0, CI [0.0, 0.0]; lane E-part status verbatim: "P-A trigger NOT met" | **NOT TRIGGERED** | `_repro/m5_selector_confirmatory.json`; M5 lane file E-part status |
| **P-B trigger** | G3 fails ONLY on the corpus ingredient, and benchmark buildable | G3 fails on corpus AND theorem; no family fails only-on-corpus (F1 fails on the cap; F2's corpus path was exercised and failed empirically; F3 fails 0/3). B5: tier-1 benchmark affordable but does not satisfy r1/S1 (synthetic precedent D2-07); tier-2 exceeds G4. | **NOT TRIGGERED** | B3 lane memo §6; B5 lane memo §2 |
| **P-C trigger** | A surviving T-part with null E-parts | No T-part survived adversarial review as a formal result: all "STATED, not proved," zero Lean lines (chair C1); M5's provable core reduces to empirical-Bayes shrinkage (M5 refuter R1); M3's T-part premise falsified at the model level | **NOT TRIGGERED** | chair C1; M5 lane refuter R1; M3 lane E-part |
| **P-D** | Part-A continuation: clean-audio / corpora / N-scaling characterization of the C1 headroom | Live — the Part-A successor track; not gated on an agentic result and not a rescue of question (ii) | **ADOPTED (Part-A successor)** | Part-A memo §A3; B3 §6; B4 §2 D-1 NO-GO action |

## 3. Outcome per lane (B.2 item 1)

- **B0 gate:** no strikes. M3 (axis a — changing q0), M5 (axis b — estimating R), M2/M4 (axis c — realization complexity) all stated admissible axes; NO-GO does not rest on B0.
- **M3 — support expansion (ran first, kill-first ordering):** **KILLED at Phase-0.** Pooled entity-match fraction **F = 0.38108 vs frozen kill threshold 0.01** — 38× over; cluster-bootstrap CI [0.24477, 0.51823]; n = 1,152 samples (36 utts × 32); 4 seed blocks consistent (0.36111/0.40278/0.38194/0.37847); greedy alone contains the target entity in 38.9% of utterances; PILESER 1.0. Artifact verdict verbatim: "M3 LANE KILLED (support already present in q0)". The information-availability premise is falsified at the model level: train-960h corpus rarity ≠ model-OOV. Residual (explicitly NOT a rescue, safeguard 8): genuinely unsupported entities exist but are the minority (SHARDURIS 0.0, CONFECTIONARY 0.0104, FARRINDER 0.0156). Phase-1 cancelled. Artifacts: `_repro/m3_phase0_selection.json` (c8bebaf), `_repro/m3_phase0_zero_support.json` (1b53b46).
- **M5 — selector accumulation (ran second):** **NO PASS, exact zero.** Dev grid: all 14 configs across 3 variant families tie at red_vs_mbr = 0.0; structural-null diagnostic ≤3/144 actionable positions (2.1%); winner V1|0.05|none from the all-tied grid per the pre-committed simplicity ordering (artifact records tie_break_applied=false: the top-ranked config already was the simplest) (`_repro/m5_selector_dev.json`). Confirmatory (single touch, designed surface: 12 speakers × 12 consecutive reading-order utts, seed 20260703, 3 replica seeds, 432 items, dev-spent + M3 ids excluded): sel_wer_8 = mbr_wer_8 = shuf_wer_8 = **0.07722 exactly**; delta_vs_mbr = 0.0, CI [0.0, 0.0] vs threshold 0.015; zero MBR picks flipped; per-position bins {1-4, 5-8, 9-12} all 0.000; ablation moot (gain_sel = gain_shuf = +0.00000, load_bearing = false); Goodhart no-fail. Verdict verbatim: "PASS(i)=False PASS(ii)=False agree=True … Route: lane result stands as measured (no PASS)." Collateral finding: MBR gains nothing over greedy on the fresh slice (−0.00003, CI [−0.00358, +0.00369]) while oracle headroom is real (+0.0238) — deployable label-free capture ≈ 0% (realized_fraction −0.0008). Artifact: `_repro/m5_selector_confirmatory.json` (freeze d4dd117, verdict f8ec1d3).
- **M2 — cross-block dependence:** design-only by pre-registration; E-part post-GO → inconclusive → NO-GO. Blind refuter: likely-dies (the effect IS the no-agency arm; occupied by Whisper `condition_on_previous_text` / WhisperX).
- **M4 — sampling intractability:** design-only; refuter likely-dies (occupied: ROVER 1997 / confusion networks / Controlled-Decoding blockwise, already in the archive); its Tier-1 dev signals are scratchpad-only and inadmissible under prereg §4 (chair C2).
- **M1 — non-separable reward:** never opened; its condition (a live M4 residue) did not obtain.
- **Timebox:** decision reached on day 1 of 10; clause (c) not needed.

## 4. Panel verdict — meta-chair reconciliation (verbatim table)

Reconciliation rule applied: disagreement defaults to "stands." No disagreements existed — both judges returned "stands" on all six charges, and each verdict was independently disk-verified. Strike check: every panel-time citation to a "B3/B4/B5 memo" was struck as unverifiable (deliverables not on disk at panel time); the strikes were outcome-changing only for C3/U2, where the defense's ANSWERS classification rested centrally on the phantom B4 decision matrix.

| Charge | Objections | Judge 1 | Judge 2 | Final | Decisive evidence |
|---|---|---|---|---|---|
| C1-tautology | P1, P2, P3 | stands | stands | STANDS | r2 verified EMPTY (delta-headroom-theory.md); _repro/m3_phase0_zero_support.json F=0.38108 vs kill 0.01, KILL=true; _repro/m5_selector_confirmatory.json sel=mbr=0.07722, delta 0.0 CI[0,0]; all T-parts "STATED, not proved," zero Lean lines; M4 B0 verbatim "zero headroom is added, U1 stands as stated"; OptSpace-notes.md:36 provenance prong unaddressed |
| C2-spread-floor-model-class | P4, P5, P6, P7, P8 | stands | stands | STANDS | No multi-backbone experiment (P4 clause B renounced; prereg note 5); m3_phase0 per-entity heterogeneity (PILESER 1.0 / SHARDURIS 0.0) loads on the model-class blade; M4 Tier-1 numbers scratchpad-only, inadmissible under prereg §4; m5 confirmatory label-free credit assignment = exact zero; D1-03/D1-04 real but external — defense's own text: "REPLACES the paper's corollary rather than defends it" (ROUTES-AROUND) |
| C3-voi | U2, U6 | stands | stands | STANDS | No B4 deliverable exists on disk (verified; phantom citations struck); named decision predicated on unrun V4 arm, no owner amendment; frozen V1\|0.05 pre-proven inert (median required lambda 60.5), exact tie predicted then confirmed — zero information ex ante; degenerate decision surface sel=mbr=shuf=0.07722; pivots P-A/P-D pre-named, reached on every branch; U6: taxonomy grep = one incidental external hit, no prediction ever made |
| C4-self-refutation | U1, U3, U4, U5, U7 | stands | stands | STANDS | m3 KILL: support already in q0 (greedy_contains_entity 0.3889); m5: zero flips, gain_sel=gain_shuf=0.0, load_bearing=false; M4 B0 "U1 stands as stated"; M2 refuter "the effect IS the no-agency arm"; r2 empty, no task-separation theorem; no decomposed/multi-model configuration ever ran anywhere in the campaign |
| C5-corpus | S1 | stands | stands | STANDS | D2 lane: r1 NOT MET across 12 verified-empty searches; MSP-Podcast fails all three load-bearing axes (D2-11); no inventory/SV-EER validation artifact anywhere (_repro/ = 6 ASR artifacts); pseudo-session substrates real but same-session/same-channel/affect-invariant by construction, and both routed-to lanes died (KILL at 38x; exact zero); B5 buildability memo does not exist |
| C6-stack-scale | S3, S4, S5, S7 (S2/S6 stipulated resolved) | stands | stands | STANDS | Repo grep: zero ECAPA/PLDA/AS-Norm/pyannote/CUSUM/BOCPD/SER/memory-graph/skill-library/RL-loop implementations in W1; S4's sentence instantiated by measurement (sel=mbr=shuf=0.07722; MBR-vs-greedy -0.00003 vs real oracle +0.0238, ~0% capture); S5 conjunctive condition 0/3 moved (no corpus, no annotation, same single 24GB GPU); all six _repro artifacts ASR — no paralinguistic spread measurement; D3-6/D3-9 corroborate S7; freeze hygiene commits c8bebaf/d4dd117/1b53b46/f8ec1d3 real but outcomes = kill/zero |

Chair summary, key sentence preserved verbatim: "Nothing at the charge or objection level: all six charges stand, 24 of 24 argued objections stand, and the 2026-07-02 NO-GO verdict is undisturbed — with several objections upgraded from projection to committed measurement by the campaign's own pre-registered instruments." Genuine verdict-neutral movements the chair recorded: S2/S6 stipulated resolved pre-panel (per-token-logprob residual still unexercised); U7's definitional prong honestly repaired (falsifiable agency observables frozen as `kill_threshold` and `load_bearing_le_50pct` artifact fields — whose extensions then measured empty); S3 materially narrowed on the selector-memory slice only, under exemplary freeze hygiene; P8's demanded finite-sample content shown to exist externally (D1-03/D1-04) but, per the defense's own admission, it replaces rather than defends the indicted corollary.

## 5. Steelman-NO-GO — point-by-point disposition (safeguard 7)

The recommendation is NO-GO; each steelman point is therefore rebutted or conceded — here, verified against the artifacts and ACCEPTED, with qualifications where the record requires them.

1. **G1 mechanically dead — ACCEPTED.** Verified: F = 0.38108 vs 0.01 (`m3_phase0_zero_support.json`, KILL = true); delta_vs_mbr = 0.0 CI [0.0, 0.0] vs ≥0.015 (`m5_selector_confirmatory.json`, PASS = false ×2); M2/M4 design-only. GO is arithmetically unavailable under the frozen conjunction.
2. **GO-minimal equally dead — ACCEPTED.** Verified: ablation block gain_sel = 0.0, gain_shuf = 0.0, retained = null, load_bearing_le_50pct = false; the second NO-GO clause is satisfied verbatim.
3. **M3 killed by its own instrument, kill predicted in advance — ACCEPTED.** Verified in the M3 lane refuter R3 (Tiglath Pileser greedy + 8/8 samples on two C1 utterances; Cinderlad in-pool; Murdoch 1/8 — all committed pre-run) and in the artifact (greedy_contains_entity_rate 0.3889; PILESER 1.0). Lane stopped per safeguard 8.
4. **M5's exact zero on a surface designed to favor the mechanism — ACCEPTED.** Verified: 12×12 consecutive reading-order design, hygiene fields (excluded_dev_spent = 144, excluded_m3_phase0 = 36), zero flips, all position bins 0.000; dev grid all-zero across 14 configs.
5. **"Instrument too weak, not mechanism" cannot carry GO-weight — ACCEPTED.** The V4 dev evidence (+0.00611, CI crossing 0) lives on dev-spent, kill-selected pools — inadmissible as confirmatory (prereg §4, §6.11); its own constructor predicts sub-threshold confirmatory results; a re-freeze requires an owner-signed amendment (safeguard 5). The confirmatory slice is spent.
6. **P-A cannot be back-doored into a de-facto GO — ACCEPTED.** Verified: "P-A trigger NOT met" verbatim (M5 lane E-part status); B5 confirms cheap-to-build was never a frozen criterion.
7. **No measurable habitat inside G4 — ACCEPTED.** Verified: 0/49 residual-headroom positions with same-speaker rare-token support (M5 lane, C1-artifact-new-analysis); ≤3/144 dev positions; 92% of residual headroom on ≤2-of-8 minority-best pools (M5 refuter R3(3)); MBR-vs-greedy −0.00003 on the fresh slice vs real +0.0238 oracle headroom.
8. **Four-for-four refuter unanimity, two-for-two mechanical confirmation — ACCEPTED.** Verified across the four mechanism lane files (all "likely-dies") and the two verdict artifacts.
9. **Delta scan strengthened the null — ACCEPTED.** Verified: D1-01 (compute-normalized single-agent ≥ multi-agent), D1-02 (debate-martingale, NeurIPS 2025 Spotlight), D1 negative findings (r2 CHECK — EMPTY as of 2026-07-03; no composition theorem; no task-separation theorem). Contested items resolve to the null under the frozen rule.
10. **r1 verified unmet on decision day — ACCEPTED.** Verified: D2 negative findings, 12 verified-empty searches; the 2026 multimodal-memory benchmark wave excludes audio (D2-05, D2-06); AFA's PAT synthetic (D2-07); MSP-Podcast undocumented/licensed/unvalidated (D2-11).
11. **Every claimed cell already occupied — ACCEPTED.** Verified: RECOVER (D3-3), FlowEdit (D2-01), contextual-biasing/phrase-hint products (M3 refuter occupied-cell check), Whisper/WhisperX (M2 refuter), ROVER/confusion networks/Controlled-Decoding (M4 refuter).
12. **Single-model pincer makes G1's no-agency conjunct structurally unsatisfiable — ACCEPTED.** Verified: M5 refuter R2/COUNT 4 (prompt-injection horn; the shuffled ablation discriminates context-vs-no-context, never agent-vs-no-agent); both horns terminate outside GO. U1 stands.
13. **B3: no family passes the three-ingredient test; P-B not triggered — ACCEPTED.** Verified against the B3 lane memo summary table (§5) and pivot disposition (§6).
14. **B4: G2 satisfied-in-form is evidence FOR NO-GO; error-cost asymmetry vindicates the frozen default — ACCEPTED.** Verified: D-1 resolved to NO-BUILD and M3 Phase-1 to CANCEL by the committed artifacts; wrong-GO ~5–7 pw sunk + a quarter of the single GPU + repeat-collapse exposure vs wrong-NO-GO bounded and reversible via r1–r3 (B4 §5). Qualification for the record: B4's recommended U2 split (ANSWERED at reduced scope) is a lane recommendation; the panel's binding ruling is U2 STANDS (chair C3), and B4 itself concurs NO-GO either way.
15. **Part-A health is not GO-weight for question (ii); its "open-and-promising" pillar has since collapsed — ACCEPTED.** Verified: Part-A memo §A2 rested on the unrun confirmatory; it ran to an exact zero. Part A continues via P-D without any agentic build (§1 above).
16. **The admissible new-information inventory is empty on the GO side — ACCEPTED.** Verified: every post-7/02 item (M3 kill, M5 dev null, M5 confirmatory zero, C1 new analyses, delta scan, B-lane memos) loads against GO on the frozen criteria.
17. **Nothing runnable inside the timebox can change the answer — ACCEPTED.** Verified: M3 stopped by kill-first rule; confirmatory slice single-touch and spent; M2/M4 E-parts frozen post-GO; M1's opening condition dead.
18. **NO-GO is the pre-registered success condition — ACCEPTED.** The campaign bought the cheapest decisive measurements (measured wall-clocks: Phase-0 1,886 s; confirmatory 25,988 s ≈ 7.2 h, per B5 §4 from the artifact elapsed fields) and both resolved for the null. Declaring otherwise would override criteria honored everywhere else.

## 6. Strongest surviving GO argument (steelman-GO) and which frozen criterion it misses (B.2 item 3)

The strongest assemblable GO case is: *G4 passes with margin (B5: all builds ≤3 pw, GPU fit demonstrated, licensing clean); G2 is satisfied-in-form with GPU receipts (B4's D-1..D-4, two rows resolved by measurement this week); F2 (accumulated-selector ASR) counts 2-of-3 on the lenient literal G3 reading (operator resolved via S2; pseudo-session corpus paths exist on disk and were exercised); and the M5 dev null is diagnosed structural (≤3/144 actionable positions), so the mechanism was arguably never given a habitat, while the constructor's V4 dev evidence (+0.00611 LOO vs MBR) hints at an amended instrument.*

Why it fails — by criterion, not persuasion:

- **It misses G1**, the load-bearing conjunct: the binding confirmatory E-part on the *designed* habitat measured delta_vs_mbr = 0.0 with CI [0.0, 0.0] against the frozen ≥0.015 + CI-LB > 0 requirement (`_repro/m5_selector_confirmatory.json`), and M3 hit its pre-registered kill 38× over (`_repro/m3_phase0_zero_support.json`). GO requires ALL of G1–G4; no strength in G2/G3/G4 can substitute.
- **The V4 rescue misses the statistical standard and the freeze:** dev-spent, kill-selected pools (prereg §4, §6.11); amendment requires owner sign-off (safeguard 5); its own constructor predicts sub-threshold confirmatory outcomes.
- **The lenient G3 reading misses safeguard 1:** ambiguity resolves against GO, and the substantive three-ingredient test fails for every family (B3 §5).
- **Even a hypothetical E-part pass would miss G1's no-agency conjunct** via the prompt-injection pincer (M5 refuter R2) — routing to P-A, whose own trigger measured 0.0.

## 7. Ledger disposition (prereg §8 — every P/U/S item)

Defense answers are classified ANSWERS or ROUTES-AROUND only (safeguard 3); final dispositions per the meta-chair.

| id | Final disposition | Adjudication basis |
|---|---|---|
| P1 | **stands** | r2 verified EMPTY 2026-07-03 (D1 negative findings); no non-separable irreducibility theorem produced; T-parts stated, not proved (chair C1) |
| P2 | **stands** | zero Lean lines added; the campaign's provable cores reduce to textbook algebra/empirical Bayes (M5 refuter R1; chair C1) |
| P3 | **stands** | no concentration-aware bound produced; M3's own kill instantiates the "support already in q0" concentration point (chair C1) |
| P4 | **stands** | no multi-backbone experiment (clause B renounced); m3 per-entity heterogeneity (PILESER 1.0 / SHARDURIS 0.0) loads on the model-class blade (chair C2) |
| P5 | **stands** — defense ROUTES-AROUND | external D1-03/D1-04 "REPLACES the paper's corollary rather than defends it" (chair C2, defense's own text) |
| P6 | **stands** | label-free credit assignment measured exact zero on the confirmatory (chair C2; `m5_selector_confirmatory.json`) |
| P7 | **stands** | no endogenous-β formulation produced (chair C2) |
| P8 | **stands** — defense ROUTES-AROUND | finite-sample content exists externally (D1-03/D1-04) but replaces, not defends (chair C2) |
| U1 | **stands** | m3 KILL (support in q0, greedy 0.3889); m5 zero flips; "the effect IS the no-agency arm" (M2 refuter); no decomposed configuration ever ran (chair C4) |
| U2 | **stands** (panel ruling) | phantom B4 citation struck; frozen selector pre-proven inert → exact tie predicted → zero information ex ante (chair C3). Record note: B4's post-panel memo (this run) documents real decisions D-1..D-4 with receipts and recommends ANSWERED-at-reduced-scope / STANDS-at-full-scope; it cannot re-litigate the panel, and B4 concurs NO-GO regardless |
| U3 | **stands** | no contribution converted plan→finding: both executed E-parts returned kill/zero; no benchmark built (chair C4) |
| U4 | **stands** | no new paralinguistic evidence; all six `_repro/` artifacts are ASR (chair C6 evidence line) |
| U5 | **stands** | the isolating ablation is moot — no gain to attribute (gain_sel = gain_shuf = 0.0) (chair C4) |
| U6 | **stands** | taxonomy made no risky pre-registered prediction (chair C3) |
| U7 | **stands**, definitional prong honestly repaired | falsifiable agency observables now frozen as `kill_threshold` / `load_bearing_le_50pct` artifact fields — whose extensions then measured empty (chair summary) |
| S1 | **contingent — UNMET** | r1 NOT MET across 12 verified-empty searches (D2 negative findings); MSP-Podcast fails the load-bearing axes (D2-11); synthetic/pseudo data non-qualifying (D2-07 precedent) |
| S2 | **resolved** (stipulated pre-panel) | llama.cpp best-of-N operator, commits b7b4b0d/cd6aa92/f9d111a; `_repro/asr_bon_llamacpp_snr5.json` |
| S3 | **contingent — materially narrowed on the selector-memory slice only** | committed code ran end-to-end twice under freeze hygiene (c8bebaf/d4dd117/1b53b46/f8ec1d3) — outcomes kill/zero; full ECAPA/PLDA/AS-Norm/pyannote/CUSUM/BOCPD/SER/memory-graph/skill-library/RL-loop stack remains unwritten (chair C6) |
| S4 | **stands — instantiated by measurement** | best honest case measured: sel = mbr = shuf = 0.07722; MBR-vs-greedy −0.00003 vs real oracle +0.0238, ~0% capture (chair C6) |
| S5 | **contingent** | 0/3 conjunctive conditions moved; discharged only within B5's three scoped routes (B5 §4; chair C6) |
| S6 | **resolved, residual open** | per-token logprob interface still unexercised (prereg note 5) |
| S7 | **stands** | measured-zero paralinguistic spread unchanged; corroborated by D3-6/D3-9; no paralinguistic artifact exists (chair C6) |

Net (unchanged from the frozen ledger, now measurement-backed): revival of the agent-level framing is gated on P1's theorem (r2) plus S1's corpus (r1) — both re-verified absent as of 2026-07-03.

## 8. Pivot disposition (B.2 item 4)

- **P-A (selector-learning-without-agency): NOT TRIGGERED.** Required ≥0.015 vs MBR with CI-LB > 0 on the fresh slice; measured 0.0, CI [0.0, 0.0]. Recorded verbatim in the M5 lane ("P-A trigger NOT met"). P-A-class single-model work remains available under its own future trigger with the named in-fence families (S6-residual logprob, frozen-judge, external frozen-LM MBR utility per D3-2/D3-10), at B5-costed ~1–2 pw — but it is not adopted as a triggered pivot of this campaign.
- **P-B (benchmark-first): NOT TRIGGERED.** G3 does not fail only-on-corpus (theorem also dead; F1 fails on the cap). B5's split stands on the record: tier-1 pseudo-session benchmark affordable (~1.5–2.5 pw) but cannot discharge S1/r1; tier-2 genuine corpus exceeds G4. The benchmark half of the moat survives NO-GO as a possible future pre-registration, not as this campaign's pivot.
- **P-C (theory-only): NOT TRIGGERED.** No surviving T-part (chair C1).
- **P-D (condition-mapping): ADOPTED — recorded as a success.** The Part-A successor: clean-audio / corpora / N-scaling characterization of the real C1 headroom (+0.0418 [0.0289, 0.0564]; hard-tail concentrated per Part-A memo A1), plus the K6 headroom-floor kill line carried forward (B4 §6). This is single-model Part-A work and makes no agentic claim.
- **Freed capacity routing (B4 D-4):** the W4 queue proceeds immediately (same-audio SSL baseline, multi-vector/trajectory emotion readout, emotion2vec fusion, W1→W4 RL-on-speaker bridge, content/language fan-out); D-3 resolves to a standing zero-cost r1 monitor (periodic re-run of the D2 negative-finding searches).

## 9. Re-open conditions (restated verbatim from prereg §2)

- **r1** — a public cross-session, same-speaker speech corpus appears;
- **r2** — a peer-reviewed non-separable decomposition bound appears;
- **r3** — a mechanism-lane kill is overturned by new literature.

Absent r1–r3, the question is **closed**. Status at decision time: r1 NOT MET (12 verified-empty searches, D2 negative findings, 2026-07-03); r2 EMPTY (D1 negative findings, 2026-07-03); r3 none (no literature item overturns the M3 or M5 kill; the delta scan loads the other way).

## 10. Citable closure sentence (for the converged paper's "deferred, not disproved" future-work question)

> The agent-level program this paper deferred is now closed by pre-registered measurement rather than by scoping: under criteria frozen in advance (pre-registration @ b19bff2), the support-expansion premise was falsified mechanically — the frozen model already emits the "rare" entities a cross-session lexicon would supply (pooled entity-match F = 0.38108 against a 0.01 kill threshold, 95% CI [0.245, 0.518]; `_repro/m3_phase0_zero_support.json`) — and cross-session selector accumulation returned an exact zero on its designed confirmatory surface (Δ vs MBR = 0.0, 95% CI [0.0, 0.0], vs a pre-registered ≥ 0.015; zero selection flips in 432 items; `_repro/m5_selector_confirmatory.json`), while both stated preconditions for revival — a public cross-session same-speaker corpus (r1) and a non-separable irreducibility theorem (r2) — were re-verified absent as of 2026-07-03; the question is therefore closed, not merely deferred, unless re-open conditions r1–r3 obtain.

## 11. Decision-Log entry (to be appended to `wiki/Decision-Log.md` upon owner ack)

`2026-07-03 — NO-GO agentic TFRL step 1: lanes M3/M5 killed at F=0.38108 vs kill 0.01 (_repro/m3_phase0_zero_support.json) and delta_vs_mbr=0.0 CI[0,0] vs ≥0.015 (_repro/m5_selector_confirmatory.json); M2/M4 design-only and M1 unopened, defaulted to NO-GO per pre-registration b19bff2 (inconclusive = NO-GO); GO-minimal failed (ablation moot, load_bearing=false); pivots P-A/P-B/P-C not triggered, P-D adopted as the Part-A successor; Part A (single-model TFRL) RATIONAL-AND-CONTINUING on the C1 oracle contrast (+0.0418 [0.0289, 0.0564]); question closed absent r1–r3; owner_ack: PENDING.`

Owner gate: this recommendation is subject to the owner gate before any publication and before WF-2 (prereg §7); `owner_verdict: PENDING`.

## 12. 中文摘要

**裁决：NO-GO —— agent 级问题关闭（问题 ii）；单模型训练无关 RL 方向维持合理并继续（问题 i，经由 P-D）。**

本决定按 2026-07-03 预注册（冻结锚点 b19bff2）§2 冻结标准逐条机械适用，零假设为 2026-07-02 深度评审的 NO-GO 裁决，规则为「不确定即 NO-GO」。

**机制车道全部未存活（G1 失败）。** M3（支持集扩张，轴 a）在 Phase-0 零支持检查处被自己的预注册杀线击杀：混合实体命中率 **F = 0.38108**，超过冻结杀线 0.01 达 38 倍（CI [0.245, 0.518]，4 个种子块一致，greedy 单独已含目标实体 38.9%）——「词表在单会话内不存在」的信息可得性前提在模型层面被证伪（语料稀有 ≠ 模型 OOV）。M5（跨会话选择器累积，轴 b）确认性实验（单次触碰、为机制特意设计的 12 说话人 × 12 连续朗读表面、432 项）测得**精确零**：sel = MBR = shuf = 0.07722，Δ vs MBR = 0.0，CI [0.0, 0.0]（预注册通过线 ≥ 0.015），记忆选择器未翻转任何一次 MBR 选择；乱序消融失去意义（增益 0/0，累积不承重）→ GO-minimal 同样失败。M2/M4 仅设计、E 部分预注册为 GO 后执行 → 按规则默认 NO-GO；M1 未开启。附带发现：新切片上 MBR 相对 greedy 增益为零（−0.00003），而 oracle 上限真实存在（+0.0238）——可部署无标签选择器对上限的捕获约为 0%。

**四个预命名转向：P-A 未触发**（测得 0.0，需 ≥0.015 且 CI 下界 > 0）；**P-B 未触发**（G3 不是仅在语料要素上失败）；**P-C 未触发**（无存活 T 部分，零 Lean 行）；**P-D 被采纳**为 Part-A 后续（C1 上限的干净音频/语料/N 扩展刻画，单模型工作，无 agent 主张），记录为成功。

**辩护团裁决**：六项指控全部成立，24/24 项异议 stands；元主席对幻影 B 备忘引用作剥离处理，仅对 C3/U2 具有结果影响力。台账处置：P1–P8、U1–U7、S4、S7 均 stands（P5/P8 辩方为 ROUTES-AROUND）；S1 或有-未满足（r1 经 12 次检索证实为空）；S3/S5 或有（S3 仅在 selector-memory 切片上实质收窄）；S2/S6 已解决（逐 token logprob 残留未验证）。

**重启条件（原文重述）**：r1 公开跨会话同说话人语音语料出现；r2 同行评审的非可分分解界出现；r3 某车道击杀被新文献推翻。三者截至 2026-07-03 均经核查为空。**否则问题关闭。** 释放的算力与人力立即转向 W4 队列与 P-D；owner 裁决待定（发表与 WF-2 前的 owner 闸门不变）。
