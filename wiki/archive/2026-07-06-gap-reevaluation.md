---
title: "GAP re-evaluation (data-anchored, by tier x organizational-form novelty x frozen fit)"
date: 2026-07-06
stage: 1-argumentation
status: "Stage-1 dataset-anchored deliverable (workflow wf_eecec38b, 6 capability + 1 probe + 2 verify + 4 synth agents). SUPERSEDES the wf_a99e2e75 pass on the same topics (this one is grounded in the actual 28-dataset inventory and uses the three-column organizational-form cut, not the cascade subtraction). Adversarial + data-grounding verified; hypothesis-grade until Stage-2. Owner review pending; wiki-sync deferred."
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# GAP re-evaluation (data-anchored)

**Stage 1 · problem-definition deliverable · 2026-07-06.** Re-ranks the prior 7-gap menu by the product **[organizational-form novelty] × [data-tier feasibility (T1>T2>T3)] × [training-free frozen fit]**, folding in the citation- and data-grounding-verifier corrections. All evidence is hypothesis-grade (Stage-1); internal numbers trace to named run artifacts (`p6_perception_delta.py`, `dec_synthesis.json`, `E10/E10b`, `M5`, `T6`), external claims to arXiv IDs. Residual uncertainty (esp. post-cutoff 2026 IDs) is marked at the end.

This re-eval does **not** issue a blanket "commodity" verdict. Each gap is cut into three columns:
- **(A) Distinct multimodal form** — the part where the frozen omni supplies decision-relevant information a text LLM structurally cannot get from any transcript (the genuine research object).
- **(B) Commodity layer** — the modality-agnostic logic a text LLM supplies once a percept/symbol is on the tape (not our research object).
- **(C) In-fence lever** — the training-free, frozen, InfoBoundary-respecting action we can actually take (element-gating/admission, new-info injection, in-contract decoding edit — **not** best-of-N read-out, which `dec_synthesis.json` + `E10b` show is oracle@N-bounded and empirically null on our surfaces).

## Scoring rubric

Each factor 1–3; rank = product.

- **Novelty N** — 3 = genuinely distinct multimodal form (info text-LLM cannot recover); 2 = partly distinct (only under a condition or at a narrow interface); 1 = commodity/modality-agnostic.
- **Data feasibility D** — 3 = **T1** (on-disk, runnable, deterministic reward today); 2 = **T2** (public, acquirable, non-leaking); 1 = **T3** (must build; no on-disk deterministic-reward surface for the sharp form).
- **Frozen fit F** — 3 = clean in-fence deployable lever with live headroom / an untested positive path; 2 = in-fence but conditioned, gated, bridge-dependent, or harness-blocked; 1 = refuted read-out (oracle@N-bounded, empirically null) or out-of-contract.

## Re-ranking table

| Rank | Gap | N | D | F | Product | Tier | Disposition |
|---|---|---|---|---|---|---|---|
| **1** | **GAP-4 ⊕ GAP-5 (merged): perception-delta / active audio re-sensing / paralinguistic-admission** | 3 | 2.5 | 3 | **~22.5** | **T1** (probes) → T3 (decisive-variable form) | **MERGE + KEEP (top bet)** |
| **2** | **GAP-7: in-contract contrastive decoding (AAD)** | 2 | 3 | 2 | **12** | **T1** | **KEEP (top lever)** |
| **3** | **GAP-3: omni decorrelated-verifier** | 2 | 2 | 2 | **8** | **T2** (+T3 seed) | **KEEP, re-scope to decorrelated / verifier-as-tool** |
| 4 | GAP-2: voiceprint cross-session memory + admission-gate | 3 | 1 | 2 | 6 | **T3** | **KEEP but PARK to W4** |
| 5 | GAP-1: best-of-N voice-agent | 1 | 3 | 1 | 3 | T1 | **DROP** (retain as commodity control) |
| 5 | GAP-6: same-model self-check | 1 | 3 | 1 | 3 | T1 | **DROP / MERGE into GAP-3 as refuted control** |

Note the deliberate tension the product captures: **GAP-4/5 wins on organizational-form novelty** (it is the *distinct research object*), while **GAP-7 wins on lever quality** (it is the only untested *bar-crossing* lever). They are complementary, not redundant.

---

## Per-gap disposition

### GAP-4 ⊕ GAP-5 — perception-delta / active audio re-sensing / paralinguistic-conditioned decision  →  MERGE + KEEP (#1)

**Why merge.** GAP-4 ("active audio re-sensing" = the agent re-invokes the raw-audio element instead of the cached transcript) is the *deployable lever* of the very object GAP-5 names (a decision conditioned on a paralinguistic/speaker/event variable). Both reduce to the `cap-perception` research object: *extract the percept + decide when it is decision-relevant + admit it into the scaffold*. They are one frontier.

**Three-column cut.**
- **(A) Distinct form:** the single capability where the frozen omni provably supplies information a text LLM cannot recover — for pure sound/music items the transcript is empty, so any omni(audio) > omni(own-transcript) delta is information-theoretic, not stylistic. Corroborated by the field's transcript-invariant minimal-pair methodology: **LISTEN (arXiv 2510.10444)** and **VoxParadox (arXiv 2605.27772)** both show audio LLMs largely fall back on the transcript and under-use acoustics; **MMAU (arXiv 2410.19168)** and **MMAR (arXiv 2505.13032)** treat front-end acoustic extraction as their own object.
- **(B) Commodity layer:** the downstream reasoning over an already-extracted, text-encoded percept ("given emotion=angry, reply empathetically") is modality-agnostic — the text-LLM tail of an ASR+SER+diarization cascade.
- **(C) In-fence lever:** the deployable perception-delta signal (`p6_perception_delta.py` — omni(audio) vs omni(own-ASR-transcript), uses only test-time info, no gold) as an **element-gating / admission router**; secondarily, **new-info injection** of the omni's own percept as a downstream element.

**Data tier — T1 for the probes, T3 for the sharp form.**
- **T1, runnable now:** `mmau-mini` (on-disk parquet, perception-delta harness already ran: **+0.117, n.s. at n=60** — internal `p6`; needs n scale-up); `crema-d` (7,442 clips, 91 acted speakers, transcript-invariant fixed 12-sentence set = the cleanest paralinguistic minimal-pair control). **Also T1:** `meld`, `vocalbench-zh` (weak probe, perception-delta 0.0).
- **T3 (no on-disk seed):** a multi-turn task where a paralinguistic/speaker cue is the *decisive* variable — a named HARD GAP; park to W4.

> **DATA CORRECTION FOLDED (high-severity).** The `crema-d` 6-way emotion gold **MUST be keyed off the FILENAME code** `{actor}_{sentence}_{EMOTION}_{intensity}` (ANG/DIS/FEA/HAP/NEU/SAD, present for all 7,442 clips). The shipped `test.csv/train.csv` `classname` column is a crowd-perceived rating that agrees with the acted label **only 46%** and is **55% neutral-skewed** — using it as reward would corrupt ~54% of labels. `crema-d` stays T1 (data+labels on disk), but the earlier "gold from csv classname" wording is deleted and aligned with the `ws3-probes` P2 warning.

**Rationale for #1.** Highest form-novelty × T1 testability × clean deployable lever. The honest Stage-1 caveat: the deployable *gain* is still directional (mmau +0.117 n.s.); the only SIG live delta (SQuAD-zh +0.283, internal `p6`) is a Chinese-ASR round-trip artifact (lexical, not paralinguistic), so it is uninterpretable as perception. The Stage-1 problem is precisely to run the **clean acoustic controls** — P3 (mmau non-speech sound+music, 667 items, transcript empty → unambiguously acoustic) and P2 (crema-d filename-keyed emotion, transcript held constant) — to establish the delta is genuinely acoustic, then test whether admission-gating harvests it. SER-as-decision-variable is a known weak spot for audio LLMs (**arXiv 2509.16589** paralinguistic-reasoning gap; **VoxEmo arXiv 2603.08936**) — a near-chance delta is a plausible and still-informative outcome.

### GAP-7 — in-contract contrastive decoding (Audio-Aware Decoding)  →  KEEP (#2, top lever)

**Three-column cut.**
- **(A/partly-distinct form:** the contrast itself (audio-present vs audio-absent logits) is multimodal-specific, but as an *organizational form* it is a decoding technique, not a new capability form — hence N=2.
- **(C) In-fence lever:** per-token contrastive decode up-weighting tokens whose logit rises when audio is present (**Audio-Aware Decoding, arXiv 2506.07233**). This is the **one untested member of the two InfoBoundary crossing-paths** — a decoding-edit. The read-out/selection levers on the other path (E7 few-shot, E8 prompt-opt, E10 two-system verifier) all **failed the +10% bar** (`dec_synthesis.json` verdict 2.2).

**Data tier — T1.** `mmau-mini` and `SQuAD-zh` are already wired in `p2_baselines.py` with on-disk audio, deterministic reward, and **real non-saturated headroom** (`dec_synthesis.json`: mmau oracle_delta **+0.147**, SQuAD-zh **+0.14** — internal).

**Frozen fit — F=2 (harness-blocked, not data-blocked).** Faithful AAD needs per-step logits from an audio-vs-no-audio forward pass, which the resident llama.cpp chat endpoint (`input_audio`, server-side generation) does **not** expose (needs a custom llama-cpp-python decode loop; the HF/int4 path OOMs on this Blackwell box). Borderline w.r.t. the strict "no structure change" contract (`elements-vs-usage §3b`). **Mandatory Mirage guard:** judge AAD against a hardened greedy(temp 0) + temperature-sweep + CoT baseline, because reported contrastive-decoding gains are often artifacts of the adaptive-plausibility constraint silently converting sampling→greedy (**Mirage, arXiv 2504.10020**).

**Rationale for #2.** The single most valuable *new* lever: T1 data, live headroom, the only in-fence path that could clear the +10% bar. Cost is **engineering (harness), not data**. Prior (`dec_synthesis` 2.2) sets an honest expectation of a null; a Mirage-survived gain would be a notable positive, and a null is still informative (closes the last in-contract read-out/edit lever).

### GAP-3 — omni decorrelated-verifier  →  KEEP, re-scope to decorrelated / verifier-as-tool (#3)

**Three-column cut.**
- **(A) Distinct form:** signal-grounded verification (quality/naturalness/prosody/emotion-match/speaker-match/paralinguistic-obedience) is a genuine distinct object — the field builds dedicated frozen-LALM-as-judge benchmarks for it, and the leading instantiation is *training-free prompt engineering* (**AudioJudge, arXiv 2507.12705**).
- **(B) Commodity layer:** lexical/content "rank-by-correctness" — self-consistency, CoT critique, weighted voting (**GenRM, arXiv 2408.15240**). In-house this is **empirically confirmed null**: `E10b` (n=40, paired-bootstrap CIs) shows the context-differentiated two-system omni verifier does **not** beat plain majority on any lexical surface (NEGATIVE −0.075 on mmau), with generator/verifier error correlation ρ≈0.5.
- **(C) In-fence lever:** best-of-N + reward-guided selection is oracle@N-bounded; the research value is specifically the **decorrelated verifier (δ_corr > 0)**, which requires a signal *independent* of the generator — i.e. **verifier-as-tool** (external acoustic/embedding feature) over verifier-as-role, the **W4 omni-embedding-as-verifier bridge (parked task #37)**. Corroborated by **Soft-SVeRL (arXiv 2605.28561)** and **FUSE (arXiv 2604.18547)** (correlated self-verifiers unreliable; decorrelated ensembling is the fix) and **One-Token-to-Fool (arXiv 2507.08794)** (naive LLM-judge reward fragility).

**Data tier — T2, not T1.** A clean *deployable* test of the distinct form uses public non-leaking preference benchmarks: **ParaPairAudioBench (arXiv 2606.24648)**, **AudioJudge (arXiv 2507.12705)**, **SpeechJudge (arXiv 2511.07931)**, **WavReward (arXiv 2505.09558)**, **EmergentTTS-Eval (arXiv 2505.23009)**. T3 build seed from on-disk `crema-d` (filename-keyed emotion/speaker, **offline scoring only — gold as reward = leakage**) + `vocalbench-zh` (whisper/quality). **Not T1:** our 28 have no task where a paralinguistic/speaker signal is the *decisive selection variable* (HARD GAP).

**Rationale for #3.** Genuine distinct object + training-free prompt-eng regime + strategic W4 bridge, but T2 data cost and payoff gated on decorrelation. Fold **GAP-6 (same-model self-check)** in here as the *refuted control* — it is the verifier-as-role null already demonstrated by `E10/E10b`.

### GAP-2 — voiceprint cross-session memory + admission-gate  →  KEEP but PARK to W4 (#4)

**Three-column cut.**
- **(A) Distinct form:** real but narrow — (i) capturing a non-text acoustic fact (ambient sound/whisper/emotion) into a memory entry, and (ii) keying/retrieving by voiceprint. Instantiated by **audiomc (arXiv 2512.14865)** "Audio-Cue Inference Memory", **MTalk-Bench (arXiv 2508.18240)**, and voiceprint-keyed multi-user memory in **AFA (arXiv 2604.25022)**.
- **(B) Commodity layer:** admission/write policy, indexing, NN retrieval, update, temporal reasoning, abstention — modality-agnostic text-memory machinery (**LoCoMo arXiv 2402.17753**, **LongMemEval arXiv 2410.10813**, benchmark **PERMA arXiv 2603.23231**). Our own `T6` confirms it empirically: the unified index reduces to a **lexical** text-embedding retrieval structure (task-purity 1.0, precision@k 0.62).
- **(C) In-fence lever:** a reward-tuned **admission policy** that WRITES the omni's own audio-cue descriptions as memory entries (InfoBoundary-permitted new-info element). Best-of-N over a fixed recalled set is bounded and, per `M5`, gave **no significant WER gain** (B6 CI [−0.0019, 0.0160], B7 CI [−0.0040, 0.0123] both cross 0; speaker ICC(1) on WER only 0.066 — the voiceprint key has little to grab on our data).

**Data tier — T3 (confirmed).** The sharpest distinct object AND the deterministic-reward surface the lever needs — **cross-session, voiceprint-keyed recall** — is a HARD GAP (no cross-session corpus; no voiceprint-keyed recall task). `audiomc` gives the audio-cue *form* at T1-for-classification but is **rubric-judged and single-session** (not oracle@N-measurable). Build seed = `crema-d` (91 gold acted speakers → synthesize per-speaker facts across sessions, retrieve keyed by voice, exact-match reward). Highest data cost of the menu.

> **CITATION CORRECTION FOLDED.** **X-Talk (arXiv 2512.18706) is DROPPED** as evidence for the speaker-keyed memory form — it is a general modular S2S framework, not voiceprint-keyed memory-bank retrieval. The sub-claim now rests on **AFA (arXiv 2604.25022) alone**, which genuinely implements voice-SID + per-user memory + persona-confusion prevention. **PERMA (2603.23231)** is re-labeled a benchmark, not a memory system.

**Rationale for #4.** Highest form-novelty tied with GAP-4/5, but crippled by T3 data cost and a null in-inventory lever surface. This is the right long-horizon W4-flagship object, not a Stage-1 quick win.

### GAP-1 — best-of-N voice-agent  →  DROP (retain as commodity control)

**Cut:** (A) none — selection over a fixed candidate set is modality-agnostic; (B/C) read-out lever, **oracle@N-bounded** (InfoBoundary, machine-checked), and `dec_synthesis.json` confirms **no deployable in-fence selector clears the +10% bar** on any live surface (minds14 saturated: greedy 0.94, oracle_delta 0.0067). **Data T1 but the lever is refuted.** Keep only as the commodity baseline other levers must beat.

### GAP-6 — same-model self-check  →  DROP / MERGE into GAP-3

**Cut:** same-weights verifier re-reading the same input = read-out, oracle@N-bounded; `E10/E10b` demonstrate it does not beat majority (NEGATIVE on mmau). **Data T1 but empirically null.** Not a standalone research object — it is the refuted verifier-as-role control folded into GAP-3.

---

## Recommendation — the 2–3 strongest bets (data-cost weighted)

1. **GAP-4 ⊕ GAP-5 (perception-admission frontier) — bet first, lowest cost.** Pure **T1**, zero new data. Run P3 (mmau non-speech sound+music delta, the sharpest "omni ≠ ASR→LLM" evidence) and P2 (crema-d **filename-keyed** transcript-invariant emotion delta) to establish the distinct object is genuinely acoustic and clean of the ASR confound; then test element-gating/admission as the deployable lever. This is the genuine multimodal research object and the cheapest to probe.

2. **GAP-7 (in-contract contrastive decoding / AAD) — highest-EV new lever.** **T1** data with live headroom; the *only* untested in-fence crossing-path. Cost is a custom logit-access decode harness (not data) + the mandatory Mirage-proof greedy+temp-sweep+CoT baseline. A Mirage-survived gain is the most consequential positive available; a null still closes the last read-out/edit lever.

3. **GAP-3 (decorrelated omni verifier, re-scoped to verifier-as-tool) — strategic, T2.** Higher data cost (public LALM-judge benchmarks) but the load-bearing bridge to the W4 flagship (#37). Pursue only the decorrelated (δ_corr>0) form; the same-weights verifier is already refuted (subsumes GAP-6).

**Park:** GAP-2 (T3, W4 flagship object). **Drop:** GAP-1, GAP-6 (refuted read-out; retain as controls).

---

## Corrections folded (audit trail)

- **Downgrade/reaffirm — data tiers:** GAP-2 **T3** (no cross-session voiceprint corpus; confirmed). GAP-3 held at **T2** (not T1 — no decisive-paralinguistic selection task in the 28). GAP-4/5 **T1** for probes, **T3** for the decisive-variable form. GAP-7 **T1**. No gap claims T1 on a hard-gap/not-runnable asset (mmsu labels-missing, mmar tarred, covost2/fleurs — all correctly excluded).
- **Deleted imagined-data claims:** (a) `crema-d` emotion gold from csv `classname` → replaced with **filename-code** key (csv agrees only 46%, neutral-skewed). (b) The RAG build recipe joining `heysquad`↔`spoken-squad` via SQuAD ids (adjacent capability, **not one of the 7 gaps**) — the disk has no shared key; if ever built it must use `spoken-squad` alone or T2 SLUE-SQA-5/NMSQA. Noted for completeness only.
- **Citation fixes:** X-Talk (2512.18706) dropped from speaker-keyed-memory evidence → AFA (2604.25022) alone; PERMA (2603.23231) = benchmark; SER "~22% recall" figure dropped as unverified (qualitative weakness kept, 2509.16589 + VoxEmo 2603.08936); LISTEN (**2510.10444**) vs VoxParadox (**2605.27772**) disambiguated; Dynamic-SUPERB (**2309.09510** / Phase-2 **2411.05361**) separated from AudioBench (**2406.16020**); SkillsBench gain **+16.6pp (33.9%→50.5%)**, arXiv 2602.12670 (relevant only to the skill-admission-gate framing, which `cap-skills` rejects as a standalone branch and folds into the perception + audio-keyed-memory frontier); Audio2Tool (2604.22821) stressor is **acoustic/noise-robustness**, not paralinguistic; OmniACBench (2603.23938) is **output** acoustic control, not input-signal-triggered behavior.

## Residual uncertainty (explicit)

- **Post-cutoff (2026) arXiv IDs unverified** (found no evidence of fabrication, but not confirmed): audiomc 2512.14865, AFA 2604.25022, ParaPairAudioBench 2606.24648, SQuTR 2602.12783, SkillsBench 2602.12670, VoxParadox 2605.27772, VoxEmo 2603.08936, OmniACBench 2603.23938, Audio2Tool 2604.22821, SpeechJudge 2511.07931, Soft-SVeRL 2605.28561, FUSE 2604.18547, ParaBridge 2606.10581. All tier decisions rest on the verified pre-cutoff subset (AudioBench 2406.16020, SLUE-SQA-5 2212.10525, SpeechDPR 2401.13463, WavRAG 2502.14727, AudioJudge 2507.12705, WavReward 2505.09558, LoCoMo 2402.17753, LongMemEval 2410.10813, LISTEN 2510.10444, MMAU 2410.19168, GenRM 2408.15240, Mirage 2504.10020, AAD 2506.07233).
- **Numeric decimals not confirmed to the decimal** from abstracts (AudioJudge 0.91 Spearman, WavRAG R@10, VoiceAgentBench 60.6%, τ-Voice figures) — read off paper tables before any Stage-2 load-bearing use.
- **Internal deltas are Stage-1 directional** (n.s. at the run n): mmau perception-delta +0.117 (n=60); SQuAD-zh +0.283 (SIG but ASR-artifact-confounded); oracle deltas 0.14/0.147. These are hypothesis-grade until re-established at Stage-2 with powered n and paired-bootstrap CIs.
- **GAP-7 is harness-gated:** its ranking assumes the custom logit-access decode loop is built; if the harness proves infeasible on the resident stack, its effective feasibility drops and GAP-4/5 becomes the sole low-cost bet.
