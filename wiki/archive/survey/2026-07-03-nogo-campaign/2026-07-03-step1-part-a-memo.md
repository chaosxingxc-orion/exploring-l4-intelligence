> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-03 NO-GO 战役），仅作历史，非现行真源。

# Step-1 Part-A memo — is single-model training-free RL rational as a direction?

> Step-1 rationality campaign lane · 2026-07-03 · workflow `wf_68e2556d-7a7` ·
> pre-registration: [[2026-07-03-agentic-tfrl-step1-preregistration]] @ freeze b19bff2. Ground rules: the 2026-07-02 verdict is the null hypothesis;
> claims tagged `delta_vs_archive` against the 17-file survey archive; every URL adversarially
> verified (0-hallucination bar). Part-A null hypothesis is INVERTED: the converged paper's positive claim stands unless undermined.

# Part-A Memo — Rationality of Training-Free RL on Frozen Omni Speech Models

Role: Part-A analyst, question (i). Null hypothesis (inverted per prereg §7 phase 2): the converged paper's positive claim stands unless undermined. All numbers below were independently recomputed from the committed artifact `projects/speech-mllm-training-free-rl/_repro/asr_bon_llamacpp_snr5.json` (n=144, 3 generation seeds × 48 disjoint utterances, pool 8, temp 0.8, SNR 5 dB, Qwen3-Omni-30B-A3B Q8_0 via llama.cpp).

## A1 — Is the demonstrated headroom real, non-trivial, condition-robust?

**Real: YES (replicates under independent recomputation).** [delta_vs_archive: new — fresh analysis of the C1 artifact, pre-registered exemption §6.4]

- Recomputed macro oracle reduction at N=8: **+0.0418** (artifact summary: `oracle_red_8 = 0.0418`, WER 0.1183→0.0765). My own 10k-resample paired bootstrap on per-utterance deltas gives CI **[0.0285, 0.0569]**, matching the committed `oracle_ci_8 = [0.0289, 0.0564]` to bootstrap noise. Not a transcription error in the paper; the artifact supports the claim.
- N-scaling recomputed exactly as committed: −0.0072 / +0.0067 / +0.0243 / +0.0418 for N=1/2/4/8, significant from N=4 (`oracle_ci_4 = [0.0122, 0.0379]`). The N=1 dip (a single temp-0.8 sample is slightly worse than greedy) is the expected order-statistics signature, not an anomaly.
- **Slice-level replication:** the 3 gen-seeds cover disjoint 48-utt slices (I verified zero ID overlap), so they are 3 independent same-direction replications: oracle-8 reduction **+0.0506 / +0.0480 / +0.0270** on seeds 42/7/123. All positive. Caveat: seed and item variance are confounded by this design (each seed = different utterances), so "3 seeds" is not 3 re-runs of identical items.
- Sanity structure: 44/144 utterances have a strictly better candidate than greedy in the pool; **0/144** are worsened by oracle-8; 14/144 have a perfect transcript greedy missed.

**Non-trivial: YES, with a concentration caveat.** +0.042 absolute is a **35% relative WER reduction** on a frozen model with no weight change. But the headroom is concentrated: my recomputation shows the **top 10 utterances (7% of the pool) carry ~50% of the total delta; top 20 carry ~76%**; 63/144 utterances are already perfect at greedy and 21/144 pools are fully degenerate (all 8 candidates identical). The effective evidence base is ~44 improvable utterances — the CI still cleanly excludes zero, but the phenomenon is a hard-tail effect, not uniform.

**Condition-robust: NO — condition-scoped, and honestly declared.** The paper concedes verbatim (`10-discussion.tex` lines 25–31) that SNR-5 was "deliberately chosen to expose measurable best-of-N headroom… because it creates spread." [duplicate — already adjudicated 7/02; zero new weight either way.] What this scopes: the +0.042 figure is conditional on (i) a noise perturbation selected for spread, and (ii) an experimental llama.cpp audio path whose absolute WERs are runtime-dependent (relative contrast is within-runtime; tex lines 16–23). Two artifact-internal observations partially soften this [new analysis, exempt]: the cleanest slice (seed 123, greedy WER 0.064 — approaching clean-ish operating points) still shows **+0.027** oracle headroom, i.e., headroom degrades roughly proportionally with difficulty but does not vanish within the artifact's own range; and this difficulty→headroom covariation (+0.051/+0.048/+0.027 vs greedy 0.158/0.133/0.064) is exactly what the spread lens predicts. No committed clean-condition artifact exists; condition-mapping is pre-named as pivot P-D (prereg §2).

**A1 holds**: real and non-trivial; condition-scoped rather than condition-robust, with the scoping being a predicted property of the mechanism (headroom tracks spread), not a contradiction of it.

## A2 — Is the realized-vs-headroom gap plausibly closable by ANY deployable selector?

**Status: OPEN — no deployable selector has yet realized a significant gain, but the strongest pre-registered test is designed and unrun, and obvious in-scope selector families are untried.**

- **MBR consensus (best measured deployable selector): null.** Artifact: `mbr_red_8 = +0.0037`, CI [−0.0082, +0.0170], n.s. at every N (~9% of headroom realized). Worse: MBR is *negative* at N=1,2 (−0.0072, −0.0068) and, per my slice recomputation, **actively harmful on the cleanest slice** (seed 123: −0.0157). [duplicate as headline; per-slice fragility is new analysis, exempt.]
- **M5 memory selectors: null on dev, but the null is diagnosed structural.** `_repro/m5_selector_dev.json` [new — post-freeze measurement]: all 14 configs across variants V1/V2/V3 achieve exactly **0.0 reduction vs MBR** on the dev-spent 144 pool. The committed structural-null diagnostic: the dev pool (random 48-utt draws) offers **≤3/144 positions** where any cross-session memory term could act; the designed confirmatory surface — `_repro/m5_confirmatory_slice_ids.json`, 12 speakers × 12 consecutive reading-order utterances, frozen winner V1|0.05|none, replica seeds 2026–2028, touched once — has **not yet been run**. So M5's pre-registered pass threshold (≥0.015 vs MBR, ~35% of headroom, CI-LB>0) is untested, not failed.
- **Goodhart guard on dev: no inversion.** True WER improves monotonically (0.1255→0.1147) as proxy score climbs (5e-05→0.559) — a mild positive for the selector program (`m5_selector_dev.json` diagnostics).
- **Untried in-scope families.** Prereg Appendix A note 5 records that **per-token logprob extraction from the GGUF was never exercised** — so frozen-model self-confidence rescoring, the most obvious label-free selector, is untested. Frozen-judge rescoring (second frozen model, no gradients) is also in-fence and untried. Gradient-trained rerankers (the paper's own "learned rerankers" future-work suggestion, tex ~114) are OUT by the scope fence.
- **Lane D3:** no current-campaign lane-D3 output exists on disk as of this search (only the 2026-06-23 pooling-method probe "D3" in `Decision-Log.md` — pre-7/02 archive, different track, duplicate, zero weight). M5 must proceed on its own committed evidence.
- **Tractability signal** [new analysis, exempt]: mean unique candidates per pool is **4.19** — the estimation problem is "pick among ~4 hypotheses," with a perfect option present in 14/144 cases; oracle selection never loses. This is the regime where ASR confidence/rescoring methods historically get partial traction.

**A2 verdict: open-and-promising** — promising in the specific sense that (i) the best pre-registered test is designed, frozen, and cheap to run, (ii) at least two in-scope selector families are untouched, and (iii) the dev null is attributable to a structural absence of session positions, not to a measured selector failure. Honest floor: every deployable selector *measured so far* is null.

## A3 — Non-empty purpose cell for the next increment?

**Non-empty, with pre-registered kill criteria (prereg §2, §5):**

1. **M5 confirmatory run** (slice committed, winner frozen) → outcome routes to GO-minimal (shuffled-memory ablation load-bearing), **P-A** (selector gain without accumulation → single-model paper #2 on closing the C1 gap), or lane kill. A named decision hinges on the result — VoI > 0 by construction.
2. **M3 phase-0 zero-support check** — entity selection committed (`_repro/m3_phase0_selection.json`: 26 pairs, 13 entities with train-960 frequency ≤5, 36 utts, clean condition, deterministic); the N=32 sampling run with its >1% kill threshold is the next cheap step (axis a).
3. **P-D condition-mapping** — clean-audio/corpora/N-scaling characterization directly discharging the A1 scoping caveat; also the paper's own named future work (tex ~113–118).
4. **Logprob-selector residual** (S6 note 5) — verifying the interface any future reward-guided decoding claim requires.

## Verdict

**Part A = RATIONAL-AND-CONTINUING** under the frozen logic. A1 holds: the headroom is real (independently recomputed, CI [0.029, 0.057] excluding zero; three disjoint slices all positive), non-trivial (35% relative), and condition-scoped in a way the mechanism itself predicts. A2 is open-and-promising (M5 confirmatory designed and unrun; structural dev null; untried in-scope families) — and independently, pivots P-A and P-D are live. The KILL condition (A1 replication failure AND best-selector null) cannot fire: A1 did not fail replication. Standing honest caveats for the adjudicator: headroom is hard-tail concentrated (top-10 utts ≈ 50% of delta); seed/slice variance confounded by design; every deployable selector measured to date is null, and MBR is harmful on the cleanest slice — the direction's rationality currently rests on the oracle contrast plus designed-but-unrun experiments, not on any realized deployable gain.