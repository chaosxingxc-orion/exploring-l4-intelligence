# Hostile round 3 on the path-B paper — 0 fundamental; 3 majors fixed (incl. a multi-seed C1 re-run)

> Third fresh hostile principle/purpose/feasibility panel (blind); meta-chair with the full round-1/round-2 ledger.
> Workflow `wf_dff3241a-d58`. The paper is now "genuinely honest, modest" with "strong reproducibility integrity"
> (Table 1 reproduces to the digit; reproduce command works; theory split correct; Goodhart correctly scoped).

## Verdict: NOT converged, but ZERO fundamental — three majors, all fixed in substance

The chair: *"the core substance is sound and the trajectory is strongly converging."* Both theory reviewers reached
**minor revision**; the integrity reviewer found the reproducibility strong. Three majors survived — two are
**stale-text leftovers** (the path-B reframe rewrote 01/02/05/07/10 but not §3 Related Work and §11 appendix), and one
is a real **methodological gap** on the flagship number:

| # | Axis | Finding | Fix (substance) |
|---|---|---|---|
| **SC-STALE-RELATED** | purpose/integrity | §3 Related Work still identified the *positive* result as "frozen bi-encoder card selection" (`:4,:9,:22`), contradicting C1 (the generative best-of-N). | Rewrote §3: the positive result is the generative best-of-N (\Cref{sec:c1}); the bi-encoder is the C2 probing operator, a *distinct* operator. |
| **SC-STALE-APPENDIX** | purpose/integrity | §11 (reward functions) still said "all selection is performed by a frozen bi-encoder ranking candidate cards" and cross-cited the **dropped SLURP** number (`:260,:270`). | Rewrote §11: primary selection = WER-driven best-of-N over generative candidates; the exact-match reward scores the secondary confounded zero-shot ablation; SLURP cross-reference removed. |
| **SC-SEED** | feasibility | C1 rested on a **single generation-seed** config with no disclosure of pool-generation variance. | **Multi-seed re-run** (seeds {42,7,123}, 48 utts each, pooled n=144; paired bootstrap now reflects utterance + pool-generation variance). Result **confirms + strengthens** C1 (below). Runner made multi-seed; artifact + all paper numbers updated. |
| minor | principle | 3 prose spots (`01:21`, `02:91`, `05:10`, `10:167`) still bound "grows with N" to spread, contradicting §5's own split. | Reworded all: lens = sign + ceiling; the N-curve is order statistics. |
| minor | principle | Baseline mismatch: the identity's baseline is the sampling mean E_q0[R], not greedy. | The multi-seed N=1 result (−0.007, a single sample *below* greedy) makes this explicit; §5/§7 now state the tilt's baseline is the sampling distribution. |

## The multi-seed C1 result (n=144, 3 generation seeds pooled) — confirms and strengthens
greedy WER **0.118**; oracle-WER best-of-N (verifiable-reward argmax, headroom): **−0.007, +0.007, +0.024, +0.042** at
N=1,2,4,8; **significant from N=4** (N=8: +0.042, 95% CI **[0.029,0.056]** — tighter than the single-seed [0.024,0.067]);
deployable MBR-consensus: **+0.004 at N=8, CI [−0.008,0.017], non-significant at every N**. The oracle headroom is
significant and robust *even accounting for generation-seed variance*; the deployable label-free selector does not
convert it into a significant gain — an honest, now-multi-seed realized-vs-headroom gap. The N=1<greedy point is the
order-statistics climb made visible (a single temp-0.8 sample is slightly worse than the greedy mode).

## Convergence read
Round 1 (fundamental: the "selection" wasn't reward-driven) → Round 2 (2 majors: over-attributed N-scaling + stale
reproduce flag) → **Round 3 (0 fundamental; 3 majors = 2 stale-section leftovers + a single-seed gap, all fixed;
the flagship survived a rigorous multi-seed re-run)**. The defect class has collapsed to *propagation + one
methodological tightening*, and the flagship number got **stronger** under the harder test. A final round-4 panel
tests convergence on the multi-seed-updated paper.
