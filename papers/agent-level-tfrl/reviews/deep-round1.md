# Hostile round 1 on the COLLAPSED (single-model) paper — NOT CONVERGED

> Fresh hostile principle/purpose/feasibility panel (blind) attacking the collapsed 21-page paper; meta-chair under
> DISCLOSURE≠RESOLUTION. Workflow `wf_89151145-3bd`. This is the first hostile round on the restructured artifact
> (Step 5 of the POMDP restructure).

## Verdict: NOT CONVERGED — 4 surviving challenges (1 fundamental, 3 major)

The chair credits the collapse for the hard substantive work (dropped generative-best-of-N / Operator-B /
thinker-talker / agent-level / cross-session claims, re-attributed the numbers, committed paired-CI artifacts,
retracted the oracle-layer emotion leak, added contamination caveats). But on the adjudicated question — is calling
frozen bi-encoder cosine card-retrieval "verifiable-reward selection / Gibbs tilting" honest? — the answer is a
**partial over-claim that must be reframed, not merely disclosed.** A real reproducible result exists underneath, so
the fix is a reframe/scope + two experiments, not a dismantling.

| # | Axis | Severity | Finding | Fix |
|---|---|---|---|---|
| **SC1** | principle | **fundamental** | The executed operator (`tool_intent.py:237,247-249`) is **argmax cosine**; the verifiable reward **never enters selection** (no β, no `exp(R/β)`, no `q*` formed). The +0.126 is an accuracy delta between **two hand-authored card wordings** (two different q0's), NOT the Gibbs gain β·KL(q0‖q\*). Title/abstract/C1/C3 frame it as verifiable-reward selection / Gibbs tilt; reward spread is never numerically measured. | Reframe honestly: zero-shot frozen-bi-encoder embedding classification / candidate-card retrieval (selection score = cosine; the verifiable reward is the EVALUATION metric + card-construction inspiration, not the selector) — **or** actually implement a reward tilt / best-of-N over model-sampled candidates. |
| **SC2** | feasibility | major | The +0.126 confounds **in-set example leakage** (the policy card injects up to 3 eval-row transcripts, `label_example_count=3`) + eval-derived boundary notes + a query-instruction change; the baseline has none. | One-factor-at-a-time ablation on the same 182 clips; draw card examples from a DISJOINT split, not eval rows; report which component drives the gain. |
| **SC3** | principle | major | The "identical machinery" bridge is false: C1 is cosine card ranking (no fitting); the paralinguistic C2 **fits a `KNeighborsClassifier`** on labeled dev embeddings with layer/pool sweep — a different, fitted operator that arguably breaks the no-fitting invariant. | Run the SAME cosine operator on paralinguistics (apples-to-apples) **or** drop the "same machinery" claim and describe C2 accurately as a fitted probe. |
| **SC4** | feasibility | major | SLURP +0.330 (0.550→0.880) — the sole cross-corpus generalization evidence, cited in abstract/intro/C1/Table 1 — has **no committed artifact, no CI, no n**. | Commit a SLURP artifact analogous to `minds14_toolintent_paired.json` **or** demote to an explicitly anecdotal, non-load-bearing mention. |

**Dismissed as non-surviving (chair):** "definitional negative billed first-class" (honest value opinion, scoped);
"lens is a tautology" (honestly labeled the DV identity used qualitatively; Lean proves exactly the two endpoints);
"near-chance understates 3× signal" (paper already reports 3.0× chance); n=182 single-seed variance (real but minor;
the +0.126 CI [0.077,0.181] is robustly off zero).

## Resolution (owner decision) → PATH B: earn the RL framing with a real best-of-N
Rather than reframe the omni-embed work down to a pure probing study (which drifts from the project's training-free-RL
thesis), the owner chose to make "training-free RL" TRUE: run a **genuine reward-driven best-of-N over model-sampled
candidates** as the primary result (C1), and demote the omni-embed candidate-card classification + the paralinguistic
probe to honest SECONDARY "encoder probing" results (explicitly NOT reward-driven RL). This resolves SC1 (a real
reward-driven selection now exists) and SC3 (the RL result and the probe are honestly distinct), and re-grounds the
reward-spread lens on the real best-of-N where the reward genuinely drives selection. SC2 (confound ablation) and SC4
(SLURP artifact/demote) are addressed as bounded fixes under the reframe. Then the hostile panel re-runs on the
re-reframed paper (POMDP loop).
