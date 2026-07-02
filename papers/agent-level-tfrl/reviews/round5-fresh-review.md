# Rigorous adversarial review — Round 3 (of the multi-round loop)

> Fresh 5-reviewer panel + meta-chair, workflow `w83xx930j` / `wf_4d21f9ae-904`. Reviewers blind to
> the resolution ledger and to prior rounds; chair armed with the full two-round ledger, reports only
> genuinely NEW critical/major. This is the third rigorous round (archives: round3 = rigorous R1,
> round4 = rigorous R2, round5 = this one).

## Headline

**The paper is now correct and honest.** The panel's most senior voice states it plainly:
*"The honesty is exemplary and I found no remaining over-claim, no hidden methodological flaw, and no
broken proof: the disclosed limitations are all genuinely disclosed."* The chair confirms:
**"No critical flaws: no theorem is wrong and no proof is broken."** Rounds 1–2 fixed every real
defect; Round 3 finds only precision/consistency and instrument-calibration items — the convergence
signature.

## Panel verdicts

| Reviewer | Recommendation | crit / maj / total |
|---|---|---|
| Senior Area Chair (accept/reject) | reject | 1 / 2 / 3 |
| Final theory checker (§5, §11) | minor revision | 0 / 1 / 4 |
| Final statistics / evaluation | major revision | 0 / 2 / 7 |
| Agent-systems realist (§8, §9) | major revision | 0 / 5 / 6 |
| Senior writing / coherence | minor revision | 0 / 2 / 3 |

**Chair verdict: major revision, NOT clean (4 genuinely new majors); 11 minors.**

## The Senior AC's "reject" — a venue-fit judgment, not a defect (chair-adjudicated)

The AC raises one *critical*: after every honest scoping move, **no single pillar clears a top
main-track novelty/validation bar, and they do not sum to one** — the theory is (by the authors' own
admission) textbook; the sole new lemma (`gain_pos_of_nonconstant`) is a one-line consequence of
strict Gibbs; the headline empirical result is a confirmatory *null* on a content bi-encoder the
system then abandons; the only positive signal (best-of-N content/intent) is standard,
contamination-flagged, and — by the paper's own `qstar_product` — *silent on the agentic thesis*; and
the system and benchmark are **designs, not executed artifacts**. The paper's own falsifiable question
(*does agentic wrapping add anything?*) is **explicitly untested**.

**Chair adjudication:** this is a *venue-fit / degree-of-realized-contribution* judgment, not a
fixable-in-text defect. The AC itself concludes the paper *"is a strong position/proposal or workshop
paper, or a main-track paper once the program in Section 9 is executed."* Since the artifact is, by
construction and by the user's instruction, a **research proposal** whose empirical validation
(Phase 2–3) is future work, executing the full agentic experiment is out of scope for "write and
review the proposal." The correct, honest response is (a) to make the *proposal* stance explicit and
foreground the open question as the motivation (AC major #2), and (b) to note that one executed
Phase-2 result would convert "plan" to "finding." The chair does **not** carry the "below-bar"
critical as a fixable new critical; it is recorded as the paper's standing, disclosed scope.

## The 4 genuinely NEW majors (chair, past the 2-round ledger) — all fixed in substance

| # | Finding | Location | Resolution (this round) |
|---|---|---|---|
| **N1** | Related Work states the "unifying abstraction" with a **reciprocal-β convention** (`F=E_q[R]−β⁻¹KL`, `q*∝q₀exp(βR)`) contradicting the paper's canonical convention and its own β-limit. | `03-related-a.tex:9` | **Fixed.** Rewritten to canonical `F(q)=E_q[R]−β·KL(q‖q₀)`, `q*∝q₀·exp(R(z)/β)`; whole section swept for `exp(βR)`/`β⁻¹`. Convention now uniform across the paper. |
| **N2** | The Lean "verification status" **table mislocates the sole documented `sorry`** — attributes it to `kl_best_of_n_le` (T2), contradicting the verbatim Lean three paragraphs below (which shows T2 is `sorry`-free and consumes the Beirami bound as a hypothesis; the `sorry` lives in a *separate* lemma). Internal contradiction in the paper's load-bearing auditable-honesty artifact. | `11-appendix.tex:35` vs `:103–108` | **Fixed.** Added a distinct lower-block row `klBoN_le_klBoundBoN_TODO` = "contains the single documented sorry (Beirami order-statistics bound)"; `kl_best_of_n_le` row = "conditional (consumes the Beirami bound as a hypothesis)". Table, prose, and verbatim Lean now agree. |
| **N3** | The pre-registered **falsification instrument is miscalibrated**: the one candidate mechanism ("Bayesian multi-session evidence integration") *is*, up to naming, textbook **PLDA / multi-enrollment** with score normalization, while the pre-registered "strongest simple" baseline it must beat is only a cosine running-centroid — so the ablation **cannot separate agentic gain from PLDA-over-cosine**. | `08-system.tex:4,8`; `09-plan.tex:24` | **Fixed in substance.** §8 names the PLDA/AS-Norm lineage explicitly and restricts the possible agentic surplus to graph curation / decay / trust-region / change-handling (*not* the posterior integration, conceded to PLDA); the pre-registered ablation win is now **arm (iii) over (ii = PLDA-over-all-enrollments)**, not over single-enrollment. §9 upgrades the primary identity baseline to **ECAPA + PLDA with full multi-enrollment**. |
| **N4** | The candidate **accumulates a posterior over AFFECT** (an accumulate-toward-a-stable-trait operator), which structurally **erases the affect-CHANGE signal** the benchmark's update/delete probe is built to detect; and its single-mechanism null is over-generalized to "the agentic claim for paralinguistics." | `09-plan.tex:45` vs `:26` | **Fixed in substance.** Mechanism **split**: identity = stable trait (integrate toward a PLDA posterior); affect = **volatile state** (per-session baseline + explicit change-point/drift detector, so "affect changed since session k" is a first-class output). Two **separate** pre-registered win/kill criteria; a null on one factor no longer generalizes to the other. |

## AC major #2 (fair, actioned as a reframe)

The AC notes the title's surprising reading ("agent wrapping adds nothing") is *unproven*, while the
proven reading is a definitional consequence of the adopted Gibbs framing. **Actioned** in
`01-intro.tex`: the paper now states early and plainly that it is a **proposal / position paper**
whose central falsifiable question is **open and is the motivation, not a result**; the contributions
frame OSA-1 as a variational identity + Hoeffding ceiling and OSA-2/`qstar_product` as an *accounting
identity* (isolated optimum = monolithic under a fixed separable reward), leaving the surprising
reading explicitly open.

## Minors (11)

Deferred per policy (non-blocking): assorted wording, cross-reference polish, and one request to
name the DER/SV-EER bands numerically in the abstract (already numeric in §9). Recorded for a
final copy-edit pass; none bear on correctness.

## Convergence read

Round 1 (6 crit + 11 maj: structural over-claim) → Round 2 (13 maj: front-matter desync) → **Round 3
(0 crit, 4 maj: convention/table precision + instrument calibration)**. The defect class is strictly
shrinking and the panel now certifies correctness and honesty. Round 4 (the cap) tests whether N1–N4
close the loop to a clean round.
