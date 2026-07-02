# Hostile round 2 on the REFRAMED (path-B) paper — SC1–SC4 resolved; 2 new majors fixed

> Fresh hostile principle/purpose/feasibility panel (blind) on the reframed paper (C1 genuine best-of-N, C2 encoder
> probing, C3 spread lens); meta-chair under DISCLOSURE≠RESOLUTION. Workflow `wf_c60021b7-fb1`. Second hostile round
> on the restructured artifact (Step 5′ of the POMDP restructure).

## Verdict: major revision (not converged); the reframe resolved SC1–SC4; 2 concrete majors survived (both fixed)

The chair confirms the path-B reframe **resolved the round-1 challenges in substance**: C1 is now a genuine
reward-driven best-of-N over model-sampled candidates from a frozen generative model (verified in
`repro_asr_best_of_n_llamacpp.py:84-92`; the β→0 tilt label is defensible); C2 is honestly demarcated as
probing/zero-shot-classification, a distinct operator, with the SLU number demoted and SLURP dropped; the
oracle=upper-bound / deployable-MBR-boundary-n.s. distinction and the experimental-audio caveat are disclosed and
adequate (both adjudicated RESOLVED). Venue-tier "reject on novelty" opinions were not counted. Two concrete,
non-disclosure defects survived and were fixed:

| # | Axis | Finding | Fix (Step 4″) |
|---|---|---|---|
| **SC-N** | principle | The N-scaling of the oracle headroom was attributed to the reward-spread lens, but the gain identity `gain=β·KL(q0‖q*)` and both Lean lemmas contain **no N** and prove only the **sign** (positive iff non-constant reward); population spread over `supp(q0)` is N-independent. The real driver is **order statistics** (`E[max_{i≤N} R]` nondecreasing in N) — and the oracle, a min-WER over a growing prefix, is N-monotone **by construction**. Flagged by 2 reviewers. | Rewrote §5 + §1 (C3) + §7: **reward-spread lens = sign + ceiling; order statistics = the N-curve**, attributed explicitly (incl. the by-construction monotonicity). Closing lens sentence restricted to sign/ceiling. |
| **SC-REPRO** | feasibility | The committed reproduce command (`repro_asr_best_of_n_llamacpp.py:22,116` + artifact) said `BON_UTTS=24`, but the committed artifact is **n=96** → the command does not reproduce the artifact. | Changed `BON_UTTS=24`→`96` in the script docstring + the `reproduce` string + both committed artifact copies. |
| minor | principle | Goodhart/over-optimization framing applied to the **oracle** reward — but the oracle *is* the true objective (WER vs reference), so there is no proxy–true gap to exploit; its only defect is non-deployability. | §10: confined Goodhart to the deployable MBR proxy / future learned rerankers; stated plainly the oracle has no proxy–true gap. |
| minor | principle | C2's read-out "pool-selection" called "selection" while C2 is asserted not-Gibbs-selection. | §7: clarified it is a read-out **configuration argmax** (layer/pooling hyperparameter), NOT model-sampled-output selection, and not a Gibbs tilt. |

**Extra honesty tightening (not required, done anyway):** the abstract now attaches "reference-based oracle reward
(an upper bound, not deployable)" to the significant +0.044 **in the same clause**, so a skim-reader cannot take the
non-deployable headroom as a deployable win.

## Convergence read
Round 1 (fundamental: the "selection" wasn't reward-driven at all) → **Round 2 (0 fundamental; 2 majors, both
clean reframe/command fixes)**. The defect class shrank from *the core mechanism is mis-framed* to *one over-attributed
theorem-scope + one stale reproduce flag*. SC1–SC4 are resolved in substance. A final fresh panel (round 3) tests
whether SC-N/SC-REPRO close the loop to convergence.
