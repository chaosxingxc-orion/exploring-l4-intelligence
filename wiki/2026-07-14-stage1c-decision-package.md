---
title: "Stage-1C Decision Package — candidate-identity dossiers from Survey v2 (owner selects on waking)"
date: 2026-07-14
role: "Assembles Survey v2 into an owner-decision-ready form. Makes NO selection. Stage-1B stays unauthorized."
inputs:
  - wiki/survey/2026-07-14-coverage-and-kill-matrix-v2.md
  - wiki/survey/2026-07-14-neighbor-matrix-v2.md
  - wiki/survey/2026-07-14-sota-cards-v2.md
  - wiki/survey/2026-07-14-scout-ledger-round2.json
  - wiki/survey/2026-07-14-search-query-log.jsonl
evidence_grade: "SCOUT round-1; 5 load-bearing kills COORDINATOR-VERIFIED (mbr-asr 2510.19471, READ 2606.04680, scaling-auditory 2503.23395, AudioToolAgent 2510.02995, jia-SER 2602.03873); 2 cites UNVERIFIED (2512.10170/2512.10403); round-2 saturation targets listed."
owner_action: "select ONE of: KILL / PIVOT-to-narrow / PROCEED-to-fresh-Stage-2-proposal / ENGINEERING-ONLY — for the study, informed by the per-identity dossiers below. Owner only."
---

# Stage-1C Decision Package

> **This package makes no decision.** It presents, per candidate identity, what the adversarial
> Survey v2 found (who occupies the cell), what survives after the challenger hunt, and a falsifiable
> three-outcome frame (proceed / pivot / kill). The owner selects. **Stage-1B is NOT authorized**;
> no dataset runs, no cross-task ρ averaging, no gold in scorers.

## 0. One-paragraph result

The adversarial hunt (15 lanes incl. 5 dedicated "kill" lanes, 305 logged queries, ~93 papers)
**killed the broad identities and left a narrow, coherent survivable core**: the **general
label-free selector (I1) is DIRECT_OCCUPIED** (MBR on frozen speech beats beam at equal-K on our
exact datasets), and audio-grounded selection (I2), abstention (I3-abstain), and agentic tool-use
(umbrella-as-system) are each **separately occupied** on audio-understanding. What **no logged paper
occupies** is the intersection object we actually named: a **supply-conditional [model × task]
realization surface ρ(c)/H(c)/regret on a weight-frozen omni** (I4 — NO_DIRECT_MATCH every lane),
the **same frozen core as both generator and audio-grounded scorer** (strict I2), **Goodhart-on-speech
+ abstain + reward-guided combined** (I3-combined), and the **full umbrella intersection** (training-free
RL ∩ frozen OMNI ∩ advantage→next-action). These survive as **working hypotheses, not proven novelty**.

## 1. Per-identity dossiers

### I1 — general label-free N-best/K-sample selector
- **Verdict: DIRECT_OCCUPIED → KILL as standalone novelty.** mbr-asr 2510.19471 (frozen Whisper,
  label-free K=64 MBR, on OUR LibriSpeech/FLEURS/CoVoST, ~31% oracle realized) [COORDINATOR-VERIFIED];
  jia-SER 2602.03873 on CREMA-D; scaling-auditory 2503.23395 on audio-understanding.
- **proceed-if**: (none — the mechanism is prior art). **pivot-if**: only survives folded into I2/I4.
  **kill**: as a headline. HAS_HEADROOM confirmed (oracle > realized) but the selection *mechanism* is owned.

### I2 — audio-grounded frozen-omni-native selector (omni core's OWN signal at decision)
- **Verdict: PARTIAL; strict form NO_DIRECT_MATCH.** Occupants use *external* scorers — READ 2606.04680
  (external TTS) [VERIFIED]; scaling-auditory (external GPT-4o verifier) [VERIFIED]; jia-SER (external
  GPT-4o). **No logged work uses the SAME frozen omni core as both generator and audio-grounded scorer
  characterized as a ρ surface.**
- **proceed-if**: the omni's own native signal (not an external TTS/GPT-4o) provides independent
  selection value AND δ_corr decorrelation is measured. **pivot-if**: only external scorers work → I2
  collapses into I1. **kill-if**: shuffling audio doesn't change selection (text-fluency artifact).

### I3 — constrained / abstaining / Goodhart-detecting selector
- **Verdict: abstain DIRECT_OCCUPIED; Goodhart-on-speech NO_DIRECT_MATCH; combined NO_DIRECT_MATCH.**
  walking-through-uncertainty 2604.25591 (frozen Qwen2.5-Omni + MMAU/MMAR/MMSU, AUROC 0.85) occupies
  abstention; inference-time-reward-hacking 2506.19248 owns Goodhart but **text-only**. No occupant
  combines reward-guided + abstain + Goodhart-detection on frozen speech/omni.
- **proceed-if**: a Goodhart breakpoint on speech N-best is demonstrable AND constraint improves
  risk-coverage over standard conformal. **pivot-if**: only abstention works (already occupied).
  **kill-if**: no speech Goodhart turning point within budget.

### I4 — (supply c, selector) cross-matrix realization surface ρ(c)/H(c)/regret
- **Verdict: NO_DIRECT_MATCH_WITHIN_LOGGED_SCOPE — the single clearest whitespace.** Nearest is
  KIT-IWSLT 2606.04730 (per-task oracle + fraction-realized across 4 speech tasks — the H(c)+ρ
  *ingredient*, but per-task, NOT supply-TYPE-stratified as a surface). Supply-type-as-design-axis
  exists only in text/recsys (ANALOGY_ONLY). **No frozen-omni [model×task] ρ(c)/H(c)/regret surface exists.**
- **proceed-if**: the surface is measurable and ρ(c) varies informatively with supply type/model/task
  (a real regularity). **pivot-if**: it is only an accounting framework with no predictive regularity →
  ENGINEERING/framework contribution. **kill-if**: ρ(c) is noise / matrix-wide headroom absent.

### UMBRELLA — training-free RL + frozen omni + agentic loop (advantage → next action)
- **Verdict: intersection NO_DIRECT_MATCH; components separately occupied.** AudioToolAgent 2510.02995
  [VERIFIED] occupies the training-free+frozen+agentic *system* (MMAU 77.5) — but the **agent does not
  access audio** (tool-orchestration, no reward-guided K-pool selection); AuTAgent 2602.13685 trains
  (not weight-frozen); JitRL is text. **Collapse risk (pre-registered): IAD 2504.01931 — an agentic
  loop beat one-shot best-of-N by only ~3–4 pts, front-loaded.**
- **proceed-if**: a frozen-omni outer loop where **reward/advantage genuinely changes the next action**
  beats one-shot best-of-N on omni tasks by a margin that survives the IAD bar. **pivot-if**: the loop
  ≈ one-shot rerank → it is test-time compute, not a new agentic-RL system. **kill-if**: no lift over BoN.

## 2. The falsifiable three-outcome frame (owner must allow all three)

For whichever identity the owner selects, the fresh Stage-2 proposal must be able to conclude ANY of:
1. **PROCEED** — a genuine cross-matrix regularity / novel object survives → fresh Stage-2 proposal.
2. **PIVOT** — only a task-specific selector family or an accounting framework survives → narrower claim.
3. **KILL** — only prior mechanisms + a metric survive → downgrade to engineering/systems or stop.
A dossier that permits only PROCEED is not a problem definition (reassessment §I).

## 3. Near-neighbor delta the umbrella MUST own (if the owner picks UMBRELLA/I4)

To not be classified as "yet another test-time-compute reranker," the eventual system must show a
delta that AudioToolAgent / AuTAgent / JitRL / scaling-auditory do NOT have, most plausibly:
**a weight-frozen omni outer loop that (a) uses the omni's OWN audio-grounded signal at decision,
(b) makes reward/advantage change the next action, and (c) is characterized by a supply-conditional
ρ(c)/H(c) realization surface across the model×task matrix** — the union of strict-I2 + I4 + the
umbrella loop. Each ingredient is occupied alone; the union is NO_DIRECT_MATCH.

## 4. Open question surfaced for the owner (not decided here)

**Agentic outer loop vs one-shot rerank.** The survey shows the value hinges on whether a real
reward-driven loop beats one-shot best-of-N on frozen omni (IAD says the margin can be small). This
is the load-bearing design fork for Stage-1C: commit to the harder agentic-loop object (higher
potential, must clear the IAD bar), or the simpler one-shot selection object (occupied for I1, open
only in the strict-I2/I4 framing). **Owner decides in Stage-1C.**

## 5. What is NOT done (honest boundaries)
- SCOUT round-1 grade; only 5 kills coordinator-verified; round-2 saturation targets are listed in the
  ledger (SER/SLU selective-prediction oracle curves; spoken-QA/agent frozen-omni K-pool selection;
  per-benchmark oracle+ρ on MMAU/MMAR/AIR-Bench; ST conformal/abstain; re-verify the 2 failed cites).
- No headroom measured by us (all HAS_HEADROOM tags are from cited papers); no Stage-1B prototype.
- No owner decision made; Stage-1B unauthorized.
