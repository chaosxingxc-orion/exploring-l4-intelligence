# POMDP restructure log — collapse W5 to an honest single-model training-free-RL-for-speech paper

> A **partially-observed decision process**. The true state s* ("the honest paper this becomes") is hidden. We hold a
> **belief b**, take the highest-information **action**, record the **observation**, **update** the belief, and
> **roll back** when an observation invalidates a prior step. Newest trajectory entry on top of the log.

## Setup
- **Trigger.** A deep 3-axis adversarial review (principle / purpose / feasibility) reached a conclusive verdict:
  the agent-level / L4 framing does not survive; most flaws are not fixable by revision. Owner: collapse to an honest
  single-model paper (Option A), executed as a POMDP.
- **Termination.** A fresh hostile panel on the restructured paper raises no surviving fundamental challenge; paper
  compiles clean; belief stabilizes. Cap 3 hostile rounds.

## Belief state b (current)
- **b.positive_spine (P≈0.7, UNVERIFIED):** single-model verifiable-reward best-of-N / reranking gives real
  content/intent gains. **BLOCKER:** the paper's opB numbers (SLURP +0.330, URO +0.335, MInDS +0.132) may have been
  produced by a remote DeepSeek API or precomputed scores, not a local frozen model (feasibility S2). → Step 1 probes.
- **b.negative (P≈0.9):** paralinguistics is a negative on the frozen omni content embedding (speaker≈chance, emotion
  null). → Step 2 firms it across models incl. a classic ECAPA reference.
- **b.theory (P≈0.6 cut / 0.4 demote):** the OSA theory is tautology-where-proven; likely cut or demoted to a
  one-paragraph honest lens. → Step 3 decides, informed by whether it does explanatory work.
- **b.agent_program:** cross-session benchmark + agent system + OSA-2/3 → future work (data frozen, stack unbuilt).
- **b.env:** local assets sufficient for Option A (4 generative bases + omni-embed bi-encoder + abundant
  content/intent/QA/paralinguistic sets); only a cross-session corpus is missing (future-work only).

## Trajectory (newest on top)
### t16 — Round-4 panel → **CONVERGED** (0 surviving fundamental/major); loop terminates
- **observation o16 (workflow wf_24d2d71f-893; chair: CONVERGED, minor revision):** all three fresh reviewers at
  **minor revision**; the integrity reviewer **reproduced every C1 number against the committed artifact to the
  digit** and confirmed the pooled multi-seed bootstrap is sound (not pseudoreplication). The chair verified the two
  round-4 "major" tags do NOT survive DISCLOSURE≠RESOLUTION: the "multi-seed confound" rested on a **code misread**
  (the 3 seeds' 48-utt subsets are near-disjoint fresh draws; the bootstrap correctly *reflects* both variances),
  and the §7 "spread grows with N" clause is a one-clause editorial slip. **Trajectory: fundamental (R1) → major
  (R2) → major (R3) → minor (R4). Zero surviving fundamental/major.**
- **editorial fixes applied anyway (chair: "should be fixed, none a blocker"):** the residual §7:15 "spread grows
  with N" clause → order-statistics climbing to a fixed ceiling; the notation table + related-work "candidate cards"
  → "candidate outputs (model-sampled transcripts)", reserving "cards" for the C2 encoder ablation; the abstract's
  C2 "pool selection" → "read-out configuration search (layer/pooling)", removing the collision with C1's best-of-N
  pool.
- **observation o16b:** compiles clean (~27.8k tokens, 0 undefined, 0 residual over-attribution). **The POMDP loop
  has CONVERGED.**
- **TERMINAL.** Belief state b ≈ hidden state s*: an honest, modest, internally-consistent single-frozen-model
  training-free-RL paper — C1 a genuine multi-seed reward-driven best-of-N (significant oracle headroom, honest
  deployable null), C2 an honest frozen-encoder paralinguistic probe, C3 a sign/ceiling reward-spread lens. Every
  number is backed by a committed, reproducible artifact.

### t15 — Step 5'' (round-3 panel) → 0 fundamental; 3 majors fixed incl. a multi-seed C1 re-run
- **observation o15 (workflow wf_dff3241a-d58; chair NOT converged, 0 fundamental, 3 majors, "strongly
  converging", "genuinely honest, modest", Table 1 reproduces to the digit):** three majors, all fixable:
  - **SC-STALE-RELATED / SC-STALE-APPENDIX:** the path-B reframe rewrote 01/02/05/07/10 but left §3 Related Work and
    §11 (reward functions) in the pre-reframe framing — still calling the POSITIVE result "frozen bi-encoder card
    selection" and citing the dropped SLURP. Internal inconsistency.
  - **SC-SEED:** C1 rested on a single generation-seed config with no pool-generation-variance disclosure.
  - + minors: 3 prose spots still bound "grows with N" to spread; a baseline-mismatch note (lens baseline = sampling
    mean, not greedy).
- **fixes (substance):**
  - SC-SEED → **multi-seed re-run** (BON_SEEDS=42,7,123, 48 utts each, pooled n=144; paired bootstrap now reflects
    utterance + pool-generation variance). Result CONFIRMS + STRENGTHENS C1: greedy 0.118; oracle N=8 +0.042 SIG
    [0.029,0.056] (tighter than the single-seed CI), significant from N=4; N=1 = -0.007 (single sample < greedy, an
    honest order-statistics detail that also answers the baseline-mismatch minor); MBR n.s. at every N (+0.004
    [-0.008,0.017]). Runner made multi-seed; committed artifact updated; C1 numbers propagated to abstract, intro,
    §5, tab:bon, §10.
  - SC-STALE-RELATED/APPENDIX → rewrote §3 + §11 so the positive result is the generative best-of-N (C1) and the
    bi-encoder is the C2 probing operator; dropped the SLURP cross-reference.
  - minors → the 3 "grows-with-N" spots split into lens(sign/ceiling) vs order-statistics(N-curve); the N=1<greedy
    result makes the sampling-mean-vs-greedy baseline explicit.
- **observation o15b:** compiles clean (~27.8k tokens, 0 undefined); no stale bi-encoder-positive framing; no stale
  numbers.
- **action chosen next:** one final convergence panel (round 4) on the multi-seed-updated paper.

### t14 — Step 5' hostile panel → SC1-SC4 RESOLVED; 2 new majors fixed (Step 4'')
- **observation o14 (workflow wf_c60021b7-fb1; chair NOT converged, 2 surviving major, both "not fatal"):** the
  reframe RESOLVED SC1-SC4 (C1 verified genuine reward-driven best-of-N; C2 honest probing; SLURP dropped;
  oracle=upper-bound / deployable-n.s. disclosed; audio caveat adequate). Two concrete defects survived:
  - **SC-N (principle):** the N-scaling was mis-attributed to the spread lens — the gain identity + Lean lemmas have
    no N and prove only the SIGN; the real driver is order statistics (E[max over N] nondecreasing; oracle is a
    min-WER over a growing prefix ⇒ N-monotone by construction).
  - **SC-REPRO (feasibility):** the committed reproduce command said BON_UTTS=24 but the artifact is n=96.
  - + 2 minors: Goodhart mis-applied to the oracle (which IS the true objective, no proxy-gap); C2 "pool-selection"
    called "selection" while asserted not-Gibbs.
- **fixes (Step 4'', substance/reframe):** (SC-N) rewrote 05-theory + 01-intro C3 + 07-feasibility to split the
  claim — reward-spread lens = SIGN + CEILING; order statistics = the N-curve (attributed explicitly, incl. the
  by-construction monotonicity); closing lens sentence restricted to sign/ceiling. (SC-REPRO) fixed BON_UTTS 24→96
  in the W1 script docstring + reproduce string + both committed artifact copies. (minors) confined Goodhart to the
  MBR proxy / learned rewards and stated the oracle has no proxy–true gap (only non-deployability); clarified C2's
  read-out tuning is a config argmax, not model-sampled-output selection. (extra) tightened the abstract to attach
  "reference-based upper bound, not deployable" to the +0.044 in the same clause.
- **observation o14b:** compiles clean — ~27k tokens, 0 undefined. 
- **action chosen next:** Step 5'' — a final fresh hostile panel to confirm convergence.

### t13 — Step 4' reframe applied → compiles clean (24pp); Step 5' next
- **action:** reframe workflow rewrote 01/02/05/07/10 to path B (C1 real best-of-N primary; C2 encoder probing;
  C3 lens grounded on C1); retitled "Training-Free RL on Frozen Omni Speech Models: Reward-Guided Best-of-N, a
  Paralinguistic Probe, and a Reward-Spread Lens"; reassembled + recompiled.
- **micro-observations (compile loop):** added alias labels `sec:c1`/`sec:c2` in 07 (the reframed sections referenced
  them). Now 0 undefined refs.
- **observation o13:** paper compiles clean — **24 pp**, ~26.5k tokens, 0 undefined citations/refs, abstract
  well-formed (single). C1 numbers verified against the artifact (greedy 0.117; oracle 0.073/+0.044 [0.024,0.067];
  MBR 0.102). SC1 resolved (real reward-driven best-of-N), SC3 resolved ("distinct operators", "no identical
  machinery" stated 7×), SC4 resolved (SLURP dropped), SC2 resolved (the confounded +0.126 demoted to an honest
  card-design zero-shot-classification note, not a reward-driven gain). No OSA-2/3/Operator-B/agentic-recovery residue.
- **action chosen next:** Step 5' — fresh hostile principle/purpose/feasibility panel on the reframed paper; chair
  decides convergence.

### t12 — GENUINE best-of-N result (n=96) → C1 anchor secured; reframing
- **observation o12 (committed `_repro/asr_bon_llamacpp_snr5.json`, W1 commit b7b4b0d):** Qwen3-Omni-30B via
  llama.cpp, LibriSpeech test-other snr5, n=96, pool 8. greedy WER **0.117**; **oracle-WER best-of-N (verifiable-
  reward argmax): significant headroom** — +0.044 at N=8 (CI [0.024,0.067]), scaling +0.013→+0.032→+0.044 for
  N=2,4,8; **MBR consensus (deployable, label-free): +0.014 at N=8 (CI [-0.0001,0.033]), boundary-n.s.** SC1
  RESOLVED: the verifiable reward genuinely drives selection over model-sampled candidates on a frozen model — real
  training-free RL, with an honest headroom-vs-realized gap. Caveats: llama.cpp audio experimental; snr5 chosen for
  measurable headroom.
- **belief update:** C1 = this genuine best-of-N (primary). C2 = omni-embed frozen-encoder PROBING (clean committed
  paralinguistic negative + an honest note that the encoder also does zero-shot SLU via candidate cards — a
  card-representation ablation, NOT reward-driven selection, a DISTINCT operator from C1); drop the confounded
  +0.126 headline (SC2) and SLURP (SC4); state C1≠C2 plainly (SC3). C3 lens now genuinely grounds on C1 (reward
  spread over sampled candidates governs the oracle headroom; N-scaling) + the C2 contrast. Two frozen models across
  the two results → frame as "frozen omni speech MODELS," not "single."
- **action:** Step 4' reframe workflow (01,02,05,07,10 rewritten; 03/11 light edits), recompile, then Step 5'
  hostile panel.

### t11 — llama-server audio API works (2.8s/gen) → genuine best-of-N running
- **observation o11:** `llama-server` (Q8 GGUF + mmproj, `-ngl 28`, resident) serves audio via the OpenAI
  `input_audio` content type; one transcription returns in **2.8 s** with the model resident. → a best-of-N loop is
  cheap (~24 utts × 9 gens × ~3 s ≈ 11 min).
- **action:** `scripts/repro_asr_best_of_n_llamacpp.py` (W1) drives the resident server: per LibriSpeech test-other
  snr5 utt, 1 greedy + 8 temp-sampled transcripts → WER vs ref → **MBR-consensus (deployable)** + **oracle (headroom)**
  vs greedy, paired-bootstrap CIs, committed artifact `_repro/asr_bon_llamacpp_snr5.json`. Running now (24 utts,
  pool 8, temp 0.8). This anchors C1 as GENUINE reward-driven training-free RL on a single frozen model.

### t10 — llama.cpp path WORKS → build the real best-of-N
- **observation o10:** `llama-mtmd-cli` loaded the Q8 GGUF + mmproj with `-ngl 28` (fits 24 GB, partial CPU offload),
  encoded the audio (436 ms), and transcribed clip 1688-142285-0055 → "Let's go see it now." Load ~3m45 (dominated by
  31 GB disk read). **Path B is feasible.** Caveat to report honestly: llama.cpp audio input is flagged
  *experimental* ("may have reduced quality").
- **action:** since load is ~3.5 min, keep the model resident via `llama-server` and drive a best-of-N client:
  per utt, 1 greedy (temp 0) + N temp-sampled (temp 0.8, varying seed) transcripts → WER vs ref → MBR-consensus
  (deployable selector) + oracle-WER (headroom) vs greedy; bounded snr5 subset; committed artifact anchors C1.

### t9 — Owner steer: run the 30B via llama.cpp (GGUF) → the int4 wall is moot
- **steer:** "qwen-omni-30B 用 llama.cpp 跑" (matches CLAUDE.md). This bypasses the HF/vLLM int4-AutoRound loader
  wall entirely.
- **observation o9 (assets found):** on disk — `models/qwen3-omni-30b-a3b-instruct-gguf/Qwen3-Omni-30B-A3B-Instruct-Q8_0.gguf`
  (31 GB) + `mmproj-…-bf16.gguf` (2.1 GB, the audio/vision projector); llama.cpp built with CUDA at `~/llama.cpp`
  (`llama-mtmd-cli` handles `--audio`, `llama-server` available). Q8 (31 GB) exceeds 24 GB VRAM → partial CPU
  offload (`-ngl`), but MoE (3B active) keeps compute cheap.
- **action:** probe `llama-mtmd-cli --audio` on one snr5 clip (greedy, `-ngl 28`) to verify the GGUF+mmproj+audio
  ASR pipeline end-to-end + timing. If OK → drive a genuine best-of-N via llama.cpp (greedy + N temp-sampled;
  MBR-consensus deployable selector + oracle-WER headroom; snr5 subset; committed artifact) to anchor C1 as real
  training-free RL.

### t8 — Path-B FEASIBILITY WALL (int4 loader), characterized → owner fork (SUPERSEDED by t9: use llama.cpp)
- **observation o8 (4 probes):** no local generative omni model runs a best-of-N on the 24 GB 5090 with the current
  stack: moss-audio-8b (custom processor `.py` missing offline), minicpm-o-4.5 (driver hardcodes Qwen3-Omni arch →
  wrong-arch failure), qwen3-omni-30b full & **thinker-only** (int4 AutoRound experts load as MISSING → HF re-inits
  them in fp32 → **58 GB → OOM**; vLLM int4 path separately crashed). **Blocker = the AutoRound-int4 LOADER, not raw
  capacity** — a correctly-loaded 30B-A3B int4 (~15 GB weights) would fit 24 GB.
- **belief update:** path B is not "reuse W1's best-of-N" (that never ran, same reason); it requires **tooling
  engineering** — wire an int4 loader (e.g. `auto-round`/`gptqmodel` inference API, likely a pip install) or a vLLM
  build that supports the quant — with uncertain payoff and a possible network install (vs the frozen-offline
  discipline). This materially changes path B's cost from the assumption under which it was chosen.
- **DECISION POINT (owner):** (1) invest in the int4-loader tooling and retry the real best-of-N (bounded but
  uncertain; may need a pip install), (2) fall back to path A (honest probing reframe — drop the RL framing, describe
  omni-embed as zero-shot classification + probing, fix SC2/SC4 — bounded, achievable now), or (3) reconsider at the
  project level. SC2/SC4 fixes apply under any path.
- **action chosen next:** surface the fork to the owner (do not unilaterally pip-install / sink more time on
  uncertain tooling without a steer).

### t7 — Step-1'(B) OBSERVATION: W1's best-of-N is scaffolding, not a result; feasibility probe underway
- **observation o7 (forensic, W1):** W1's ASR best-of-N is **genuine by design** (samples N from Qwen3-Omni-30B via
  `generative_omni.py`; selectors = **oracle-WER** (upper bound) + **MBR consensus** (the only deployable selector);
  no reward model/reranker). BUT **no run ever completed**: the sole artifact is degenerate (2 clean utts, all
  WER 0.0, zero gain); the HF 30B run **stalled loading** on the 24 GB laptop 5090; the vLLM run **crashed**
  (auto-round int4 engine-init); scripts are **untracked**, artifact **gitignored**, README numberless. So path B has
  no ready anchor — a genuine best-of-N must be **made to complete** on a model that fits 24 GB, reporting the
  DEPLOYABLE MBR gain vs greedy (oracle-BoN shown separately as headroom).
- **belief update:** path B feasibility hinges on getting a local generative omni model to load + sample + complete
  on 24 GB. The 30B-A3B (24.5 G int4) is borderline/OOM; smaller candidates (moss-audio-8b 16.9 G, minicpm-o 18.7 G)
  may fit but the driver is Qwen-shaped (processor/chat-template compatibility uncertain).
- **action:** feasibility probe — load the smallest generative model (moss-audio-8b) via the driver + one greedy
  transcript on a staged snr5 clip. If it works → run a real best-of-N (greedy vs MBR vs oracle, snr5 subset,
  committed artifact) to anchor C1. If all local generators fail on 24 GB → report the feasibility wall + options.

### t6 — Owner DECISION: path B (earn the RL framing with a real best-of-N)
- **decision:** run a GENUINE reward-driven best-of-N over MODEL-SAMPLED candidates so "training-free RL" is a true
  thesis; omni-embed candidate-card classification + the paralinguistic probe become SECONDARY "encoder probing"
  results (honestly described, not RL). Fixes SC1 (real reward-driven selection now exists), SC3 (the RL result and
  the probe are honestly distinct), and re-grounds the spread lens on the real best-of-N.
- **enabler to verify:** W1 (`projects/speech-mllm-training-free-rl`) has `repro_asr_best_of_n_vllm.py` + a
  `_repro/asr_bon_other_rows.json` artifact — a vLLM ASR best-of-N on LibriSpeech. If it genuinely (i) samples N
  hypotheses from a LOCAL generative model and (ii) selects by a VERIFIABLE reward (WER/oracle or a reward proxy),
  it is real training-free RL and can anchor C1. Investigating now.
- **plan:** (1) verify + (if needed) re-run W1 ASR best-of-N → committed artifact; (2) reframe the paper: primary =
  real best-of-N (reward-driven selection over sampled candidates); secondary = omni-embed zero-shot SLU
  classification + paralinguistic probe (honest, not RL); fix SC2 (confound ablation) + SC4 (SLURP artifact/demote);
  (3) re-run Step 5 hostile panel on the re-reframed paper.

### t5 — Step 5 (fresh hostile panel) → NOT CONVERGED; a belief-invalidating framing finding
- **action:** fresh hostile principle/purpose/feasibility panel (blind) attacks the collapsed paper; chair under
  DISCLOSURE≠RESOLUTION (workflow wf_89151145-3bd).
- **observation o5 (verified against committed code):** NOT converged, 4 surviving:
  - **SC1 (fundamental/principle):** the executed operator (`tool_intent.py:237,247-249`) is **argmax cosine**; the
    verifiable reward **never enters selection** (no β, no `exp(R/β)`, no `q*` formed). The +0.126 is an accuracy
    delta between **two hand-authored card wordings** (two different q0's), NOT the Gibbs gain β·KL(q0‖q\*). So the
    title/abstract/C1/C3 framing "verifiable-reward selection / Gibbs tilting / best-of-N" is a **partial over-claim**
    even after the collapse — the method is honestly **zero-shot frozen-bi-encoder embedding classification /
    candidate-card retrieval** (reward = eval metric + card-construction inspiration, not the selector).
  - **SC2 (major/feasibility):** the +0.126 confounds **in-set example leakage** (policy card injects up to 3
    eval-row transcripts) + boundary notes + a query-instruction change → needs a one-factor-at-a-time ablation with
    card examples from a DISJOINT split.
  - **SC3 (major/principle):** the "identical machinery" bridge is false — C1 is cosine ranking (no fitting); C2 is a
    **fitted kNN** probe → drop the "same machinery" claim or run the same operator on paralinguistics.
  - **SC4 (major/feasibility):** SLURP +0.330 has **no committed artifact / CI / n** → commit one or demote to anecdotal.
- **belief update (invalidation):** even the collapsed "training-free RL selection" framing OVER-CLAIMS relative to
  what the omni-embed code does. Twice now the "training-free RL" framing has failed against the code (agent →
  selection → really zero-shot classification + fitted probing). The honest description of the omni-embed experiments
  is a **representation-probing / zero-shot-SLU study**, NOT reward-driven RL. A genuine "training-free RL" result
  would require an ACTUAL reward-tilt / best-of-N over MODEL-SAMPLED candidates (which W1's ASR best-of-N does, but
  the omni-embed pipeline does not).
- **DECISION POINT (owner's call — not auto-pivoting a 3rd time):** reframe-to-probing (honest, bounded, but drifts
  from the project's training-free-RL thesis) vs earn-the-RL-framing-with-a-real-best-of-N (thesis-faithful, larger)
  vs step back at the project level. Fixes SC2/SC4 (bounded pilots) apply under any path.
- **action chosen next:** ask the owner the fork; then iterate (Steps 3–5 loop) on the chosen framing.

### t4 — Step 4 (restructure) → compiles clean; cut verified
- **action:** parallel rewrite of 8 sections to the collapsed thesis (shared spec); deleted 06-convergence /
  08-system / 09-plan; retitled to "Training-Free RL as Verifiable-Reward Selection on a Single Frozen Speech
  Model: …"; reassembled + recompiled.
- **micro-observations (compile loop):** fixed a stray `\end{abstract}`, a `\Var` undefined macro (which exposed a
  real spread-definition inconsistency — spread was defined as variance in prelim vs range elsewhere; unified to the
  RANGE with variance as the leading-order proxy), and two dangling table refs (`tab:opB`→`tab:content`,
  `tab:cremad-matrix`→`tab:para`).
- **observation o4:** paper compiles clean — **21 pages** (down from 57), ~22.7k tokens, 0 undefined citations/refs,
  no fatal errors. Cut verified: no residual OSA-2/3, agentic-recovery, Operator-B, thinker-talker, or
  stability-tax claims (only the project name in the author line contains "L4"). All agent/generative-operator
  mentions are honest negations / future-work.
- **belief update:** the collapsed paper now states the collapsed thesis end-to-end (abstract, 3 contributions,
  spread lens, results with correct attribution, honest negative, future work). b.paper ≈ stable pending the Step-5
  hostile-panel observation.
- **action chosen next:** Step 5 — fresh hostile principle/purpose/feasibility panel on the RESTRUCTURED paper,
  under DISCLOSURE≠RESOLUTION. If a surviving fundamental challenge → iterate/rollback; else terminate.

### t3 — Step 2 (negative probe) + Step 3 DECISION (theory's fate)
- **action:** bounded GPU run of `paralinguistic_negative_probe.py` (frozen omni-embed, CREMA-D, speaker 91-way +
  emotion 6-way, dev-selected layer, 3 seeds, bootstrap CI vs chance).
- **observation o3 (committed `_repro/paralinguistic_negative_probe.json`):** SPEAKER mean acc **0.033** (range
  0.023–0.047) vs chance 0.011 → **3.0× chance** (near-chance, but honestly *above* chance — not "at chance");
  EMOTION mean acc **0.405** (0.387–0.42) vs chance 0.167 → **2.4× chance** (real-but-modest). Combined with the
  committed pool-selection null (emotion training-free gain CI [−0.043,+0.116]): training-free selection over this
  encoder yields **no significant paralinguistic improvement**.
- **belief update:** the honest negative is now precise and committed — the frozen omni CONTENT read-out carries
  near-chance speaker and modest emotion, with **low exploitable paralinguistic spread**. This directly supports the
  spread lens: content/intent has HIGH reward spread (MInDS +0.126 SIG) → selection gains; paralinguistics has LOW
  spread → no gain.
- **Step 3 DECISION (theory's fate):** the OSA-1 *spread lens* **earns its place** — it does real explanatory work on
  the fresh data (content-vs-paralinguistic contrast). So: **KEEP** OSA-1 as one short section (the identity
  gain=β·KL(q0‖q\*) + the honest caveat that it is the Donsker–Varadhan identity, used qualitatively; + the strict
  Lean lemmas gain_eq / gain_nonneg / flat_no_gain / gain_pos_of_nonconstant / kl_pos_of_ne as an honest
  formalization). **CUT from the paper's claims:** OSA-2/3 (qstar_product, gain_product, rollout_deficit) — the
  agent-decomposition theory the principle read showed to be exp-additivity tautology. (Lean file can retain them
  sorry-free but the paper no longer cites them as contributions.)
- **action chosen next:** Step 4 — restructure the sections to the single-model thesis (parallel rewriters on a
  shared collapsed-thesis spec), recompile, then Step 5 hostile panel.

### t2 — Step 1 CLOSE (MInDS re-run) → belief correction (a rollback of my own suspicion)
- **action:** bounded GPU re-run of `repro_minds14_toolintent.py` (frozen omni-embed bi-encoder, MInDS-14 en-US,
  n=182, seed 42, 3 arms + paired bootstrap).
- **observation o2:** naive=0.720, raw-schema=**0.857**, policy=**0.984**; **policy vs raw-schema = +0.126
  [+0.077,+0.181] SIG** (24 fixes, 1 reg); policy vs naive = +0.264 [+0.198,+0.335] SIG. Artifact committed:
  `_repro/minds14_toolintent_paired.json` + reproduce command.
- **belief correction:** the provenance agent's suspicion that MInDS 0.984 was "MRR misread as Acc@1 0.972" is
  **WRONG** — the policy arm's Acc@1 really is 0.984, and the paper's `0.852→0.984 (+0.132)` is essentially the
  reproduced `0.857→0.984 (+0.126)`. So I **roll back** my planned "cut/replace the MInDS number" action: the NUMBER
  is real and now reproducible-with-a-committed-artifact. What remains genuinely wrong is only (a) the **mechanism**
  attribution (bi-encoder selection, not generative best-of-N) and (b) the **baseline label** ("raw-schema arm
  0.857", not "bare intent-name 0.550"). This is the POMDP paying off: probing corrected a belief I would have
  wrongly acted on.
- **positive-spine status:** SOLID — MInDS is a real, local, frozen-model, verifiable-reward SELECTION gain with a
  committed paired-CI artifact. Sufficient to anchor the collapsed paper's positive result.
- **positioning risk (for Step 4/5):** the collapsed thesis ("frozen-model verifiable selection for speech intent")
  sits near W1's territory (best-of-N/reranking) — the paper must state how it differs (omni-embed encoder + the
  paralinguistic negative + the spread lens, on SLU/intent, not W1's ASR best-of-N). Note for the hostile panel.
- **action chosen next:** Step 2 — signal probe (firm the paralinguistic negative across omni-embed + a classic
  ECAPA reference), then Step 3 (theory's fate).

### t1 — Step 1 OBSERVATION (provenance trace) → belief update
- **observation o1 (forensic, cited):** the three content/intent numbers are produced by the **frozen omni-embed
  bi-encoder** doing cosine retrieval over static text candidate-cards under a verifiable reward
  (`evaluation/tool_intent.py:237,247,258`; `SentenceTransformer(omni-embed-nemotron-3b)`; grep for any local
  generation primitive = **0 matches**). So they are **LOCAL-FROZEN** and honestly keepable — BUT:
  1. **Mis-attributed.** The paper sells them as "generative candidates … Operator-B (Z_B) … best-of-N"
     (`07-feasibility.tex:74`, table caption `:78`, Z_B defined as the thinker–talker `:11`). Reality = a frozen
     **bi-encoder (Operator-A-class) selection over hand-authored cards**, not a generative policy, not best-of-N
     decoding. → must re-word, not cut.
  2. **URO `+0.130` rerank IS remote DeepSeek** (`uro_qa_low_margin_rerank.py:343-344`) — cut or re-run local.
     (The URO `+0.335` base retrieval is local and keepable; the remote step is a separate bracketed rerank.)
  3. **MInDS `0.852→0.984 (+0.132)` is unbacked** by any committed artifact and looks like MRR 0.984 misread as
     Acc@1 0.972; artifact-backed gain is **+0.089 (0.883→0.972)**. → correct or cut.
  4. **No committed score file** for any of the three (only `_repro/emotion_pool_paired_v2.json`, the null). Numbers
     live only as prose in `docs/`. → not reproducible until re-run + committed.
- **belief update:**
  - b.positive_spine: **CONFIRMED real + local**, P≈0.9 — but it is *frozen-bi-encoder verifiable SELECTION*
    (embedding-candidate reranking), **not** generative best-of-N. The "two-operator (embedding vs generative)"
    framing is moot: the reproducible local results are all Operator-A-class selection; the generative operator was
    never run locally. → the collapsed paper's thesis becomes **"training-free RL as verifiable-reward selection on a
    single frozen speech model."**
  - NEW substantive defects to fix in Step 4: (a) re-attribute all three (bi-encoder selection, not generative
    best-of-N); (b) cut the remote-DeepSeek URO rerank from any all-local claim; (c) replace MInDS +0.132 with the
    artifact-backed +0.089; (d) commit reproducible score artifacts.
- **action chosen (closes Step 1):** a **bounded GPU re-run** of the bi-encoder content/intent selection on SLURP +
  MInDS (the clean tasks) to (i) regenerate committed score JSONs + reproduce commands, and (ii) resolve the MInDS
  number honestly from the artifact. Then Step 2 (signal probe) firms the negative.

### t0 — INIT
- **belief:** b0 as above (from the 3-axis diagnosis, archived in `reviews/deep-review.md`).
- **action chosen:** Step 1 — provenance pilot (highest information value: it gates whether Option A has a positive
  empirical spine or must slide toward a negative-results paper).
- **observation:** o1 above.
