# Rigorous adversarial review — Round 4 (THE CAP)

> Fourth (and final, per the pre-registered 4-round cap) fresh 5-reviewer panel + meta-chair,
> workflow `wecbfsty3` / `wf_368c69ce-f3d`. Panel blind to prior rounds and the ledger; chair armed
> with the full 3-round ledger. Archives: round3 = rigorous R1, round4 = R2, round5 = R3, round6 = R4.

## Headline

**The math is confirmed sound and the emotion NULL reproduces exactly.** A blind theory referee
re-derived the Gibbs tilt, the gain identity `gain=β·KL(q0‖q*)`, the `spread²/(8β)` ceiling, the
`Var/(2β)` refinement, and the product factorizations, and checked the two new strict lemmas
(`gain_pos_of_nonconstant`, `kl_pos_of_ne`) are genuinely sorry-free in the real `OptSpace.lean`; a
blind statistics hawk confirmed every emotion statistic against `emotion_pool_paired_v2.json`
(mean +0.037, t-CI [-0.043, +0.116], 2/5 per-seed CIs exclude 0, seeds {42,7,123,2024,31337}). Chair:
*"No theorem is wrong and no proof is broken."* All 7 new findings are internal-consistency / fidelity
/ artifact-integrity defects — **fixable without new science** — with the **same root cause as round 2**:
incomplete propagation of the reframe into the most-read anchors + the cited Lean artifact's prose.

## Panel verdicts

| Reviewer | Recommendation | crit / maj / total |
|---|---|---|
| Adversarial theory referee (measure/prob + Lean 4) | minor revision | 0 / 2 / 4 |
| Adversarial statistics / empirical-methods | major revision | 0 / 3 / 6 |
| Adversarial agent-systems + evaluation realist | minor revision | 0 / 3 / 6 |
| Adversarial novelty/positioning + citation forensics | major revision | 0 / 5 / 8 |
| Adversarial reproducibility + coherence auditor | minor revision | 0 / 3 / 6 |

**Chair verdict: major revision, NOT clean (7 new major, 0 critical); 14 minors.** This is the 4th
round — the pre-registered cap — so the loop terminates here with these 7 fixed in substance (no round 5).

## The 7 genuinely NEW majors — all fixed in substance

| # | Finding | Fix (this round) | Verified |
|---|---|---|---|
| **NM1** | Contribution **C1 scrambles the concentration inputs** — attaches Pinsker to the `spread²/(8β)` ceiling and Beirami to the regret, the exact reverse of `rem:honesty`, the appendix table, and the Lean source. Flagged **independently by 3 reviewers**. | `01-intro.tex`: rewritten so each input attaches to exactly one theorem — ceiling (`gain_le_of_hoeffding`) ← Hoeffding alone (discharged on paper); best-of-N KL bound (`kl_best_of_n_le`) ← Beirami order-statistics = the single `sorry`; regret (`regret_O_sqrt_log`) ← Pinsker (named hypothesis). | "rests on Hoeffding's lemma alone" present; wrong mapping absent |
| **NM2** | **The cited `OptSpace.lean` still carried pre-correction docstrings** ("enlarging the space by isolated agents strictly adds optimization headroom"; "restoring convergence to qstar") contradicting the corrected `qstar_product` thesis. Flagged by 2 reviewers. | Edited the docstrings/comments (not the theorem statements): `gain_product` now framed as an additive **decomposition of a fixed** optimum (isolation buys **no** headroom; extra gain requires a new non-degenerate reward); "restoring convergence" → "motivates slow drift; finite-time convergence left open". **`lake build` re-run: 8559 jobs, sorry-free.** | rebuilt sorry-free; 0 prose leaked to paper |
| **NM3** | **Artifact-integrity:** the committed JSON's headline `across_seed_ci95_t` + NULL verdict were **NOT emitted** by the cited reproducer (`pool_method_probe_paired.py` computed only the std) — the t-CI was hand-inserted; re-running would overwrite + strip it. | Added the across-seed one-sample t-CI (`scipy.stats.t`) + `across_seed_significant` + the NULL verdict string to the script's summary; **re-ran on GPU (RTX 5090)**: reproduced mean +0.037, t-CI **[-0.043, +0.1163]**, NULL, 2/5 — identical per-seed deltas — now genuinely script-emitted. | GPU re-run byte-matches (modulo `elapsed_s`) |
| **NM4** | **Asymmetric baseline:** round-3 upgraded the identity baseline to ECAPA+PLDA, but the **affect baseline was left as differencing+threshold** (not a classical online CPD), so arm (iii)'s change-point win would be un-attributable — the exact strawman the identity upgrade avoided. | `08-system.tex` + `09-plan.tex`: affect baseline upgraded to the **strongest classical online CPD** (CUSUM / BOCPD, PELT upper reference; dev-selected hazard) over the SER-posterior stream; the agentic store must strictly exceed it. Propagated through the milestone table + release-artifact list. | 8 CPD mentions; differencing-strawman removed |
| **NM5** | **§8 defined a conjunctive win** (identity AND affect-change) contradicting §9's per-factor independent falsifiers. | `08-system.tex`: win rewritten **per factor and independently** — an identity win (iii>ii on SV/SID) and, separately, an affect-change win (iii>ii on the probe); "we do not require the conjunction". | per-factor phrasing present |
| **NM6** | The appendix "**verbatim**" `kl_pos_of_ne` block **weakened `hp` from `0 < p z` to `0 ≤ p z`** — overstating the machine-verified generality on the paper's central honesty claim. | `11-appendix.tex`: quoted signature made byte-identical to source (`0 < p z`, `0 < r z`, `∃ z, p z ≠ r z`); `gain_pos_of_nonconstant` `hR` matched to `∃ z w, R z ≠ R w`; prose adjusted. | strict `0<p` verbatim present |
| **NM8** | §9 asserted **PLDA "equivalently cosine with AS-Norm"** — technically false (PLDA is a generative latent scorer; AS-Norm is a normalization layer atop cosine) and inconsistent with §8. | `09-plan.tex`: "equivalently" deleted; identity baseline = **the stronger of {multi-enrollment PLDA, cosine+AS-Norm}, dev-selected**; AS-Norm described as a score-normalization layer, matching §8. | 0 "equivalently, cosine" |

## Ledger dispositions (re-raised items the chair did NOT count as new)

- **already-scoped:** Op-B single-seed positives + SLURP/MInDS provenance (Phase-0 deliverable, R1).
- **already-resolved:** jitrl2026 peer-review status (R1); emotion NULL reporting via t-CI (F6, R2).
- **invalid:** title "…Not Agent Wrapping" reads the disclosed-open positioning as a settled claim (it
  is the proven accounting-identity reading, with the surprising reading explicitly left open);
  `rlvrincentive2025` "reversal" rests on a defensible title reading.
- **minor (not fixed):** the speaker probe "at chance" phrasing (0.04 vs 0.011 chance) — the
  substantive claim (no load-bearing paralinguistic retrieval) is already established; wording noted.

## Convergence read — terminal

Round 1 (6 crit + 11 maj: structural over-claim) → Round 2 (13 maj: front-matter desync) → Round 3
(0 crit, 4 maj: convention/table precision + instrument calibration) → **Round 4 (0 crit, 7 maj:
anchor-propagation + artifact fidelity)**. **No critical since round 1; no broken math or proof in any
rigorous round.** The residual defect class is purely *propagation/fidelity* — the reframe reaching the
last anchors and the cited artifacts. All 7 fixed in substance; the loop terminates at the pre-registered
4-round cap with a paper that is internally consistent, machine-checked sorry-free (bar the one documented
Beirami `sorry`), and whose every reported number is now emitted by its committed reproducer.
