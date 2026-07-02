# Hostile round 4 — CONVERGED (0 surviving fundamental/major)

> Fourth (final) fresh hostile principle/purpose/feasibility panel on the multi-seed-updated path-B paper;
> meta-chair with the full 3-round ledger. Workflow `wf_24d2d71f-893`.

## Verdict: CONVERGED — minor revision

**All three fresh reviewers independently recommend only minor revision.** The reproduction-grounded integrity
reviewer **re-verified every headline C1 number against the committed artifact to the digit** (greedy 0.118≈0.1183;
oracle −0.007/+0.007/+0.024/+0.042 at N=1/2/4/8 ≈ artifact; N=8 WER 0.077≈0.0765, CI [0.029,0.056]; SIG from N=4;
MBR +0.004 [−0.008,0.017] n.s.), confirmed the N=1<greedy / sampling-mean baseline is handled honestly everywhere,
that the pooled 3-seed bootstrap is legitimate (fresh utterance draw per seed, n=144 distinct rows — not
pseudoreplication), that SLURP is cleanly dropped, and that the lens=sign/ceiling vs order-statistics=N-curve split
is correct in intro/§5/§7/§10/conclusion.

**Chair triage — the two round-4 "major" tags do NOT survive DISCLOSURE≠RESOLUTION:**
- *"Multi-seed variance confound"* (Speech reviewer, major): rests on a **factual code misread** — the reviewer
  assumed the three seeds' 48-utt subsets are enforced-disjoint and the CI is a single utterance-level draw. The
  chair read `load_utts` (`repro_asr_best_of_n.py:49`): each seed draws a fresh permutation, the subsets are
  near-disjoint by chance, and the paper's claim that the pooled bootstrap *"reflects both per-utterance and
  pool-generation variance"* is TRUE. Non-surviving.
- *"§7 spread-grows-with-N clause"* (Integrity reviewer, major): a genuine but **one-clause editorial slip**
  contradicting the paper's own (correct, repeated) N-independence-of-spread statement — non-blocking; fixed.

**Editorial fixes applied (chair: "should still be fixed before submission, but none is a blocker"):**
1. §7:15 residual "spread grows with N" clause → rewritten so the N-growth is order statistics climbing to a
   **fixed** (N-independent) spread ceiling.
2. Notation table (§11) + related-work (§3) "candidate cards" → "candidate outputs (model-sampled transcripts)";
   "cards" now reserved for the C2 encoder ablation.
3. Abstract C2 "pool selection" → "read-out configuration search (layer/pooling, not selection over model-sampled
   candidates)", removing the collision with C1's best-of-N pool.

## Convergence
**fundamental (R1) → major (R2) → major (R3) → minor (R4), CONVERGED.** Zero surviving fundamental/major across a
fresh, blind, code-verifying panel. Every headline number is backed by a committed, reproducible artifact; the
flagship survived — and tightened under — a rigorous multi-seed re-run. The multi-round adversarial loop on the
path-B paper terminates here.
