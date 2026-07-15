> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-03 NO-GO 战役），仅作历史，非现行真源。

# Step-1 B-lane memos — B3 task-family / B4 VoI / B5 feasibility

> Campaign lane record · workflow wf_f6d37987-df5 · prereg @ b19bff2. Written to disk to make
> every decision-doc citation resolvable (integrity-check finding #1).


## B3 — task-family ingredients check (three-ingredient test per prereg G3)

**Verdict:** NO-GO from the B3 axis: no candidate task family passes all three ingredients. Content personalization fails (c) — the single-session cap premise died at M3 Phase-0 (F=0.38108 vs kill 0.01). Accumulated-selector ASR is the closest (passes (a) and (c)) but ingredient (b) is measured hollow on all available/buildable data and its binding confirmatory E-part is an exact zero (sel=MBR=0.07722, zero flips) — under "inconclusive = NO-GO" it cannot carry GO-weight. Cross-session paralinguistics fails 0/3 (S7 flat reward; S1/r1 no corpus, D2 re-verified empty 2026-07-03; no measurable cap). No lane-suggested family substitutes. P-B is NOT triggered (no family fails only on corpus); P-A trigger NOT met per the committed artifact. All post-7/02 evidence admissible for GO-weight points against GO.

# B3 lane memo — task-family ingredients check (three-ingredient test)

> Step-1 rationality campaign · 2026-07-03 · prereg: `wiki/2026-07-03-agentic-tfrl-step1-preregistration.md` @ freeze b19bff2 (§2 G3, §5 thresholds, §8 ledger). Null hypothesis: the 2026-07-02 deep-review NO-GO (`papers/agent-level-tfrl/reviews/deep-review.md`). Inconclusive = NO-GO. GO-weight only for evidence unavailable on 7/02. Scope fence applied throughout: gradient-trained selectors/rerankers/probes OUT (prereg §3).

## 0. Test definition and its relation to the frozen G3

Per my task, each candidate family is tested on three ingredients: **(a)** a verifiable reward exists; **(b)** cross-session structure exists on AVAILABLE OR BUILDABLE data (the dataset freeze is POLICY — planned lockfile expansion is allowed, per prereg §2 P-B; but D2's r1 re-check is binding evidence on what exists publicly); **(c)** a demonstrated single-session cap (something a cross-session operator could add that single-session operation provably/measurably lacks).

Relation to the literal frozen G3 (operator / corpus / theorem, ≥2 required): the **operator** ingredient is resolved globally for ASR-direction families (S2 resolved — llama.cpp best-of-N on frozen Qwen3-Omni-30B; prereg §8 note 2; artifact `projects/speech-mllm-training-free-rl/_repro/asr_bon_llamacpp_snr5.json`). The **theorem** ingredient points at "the G1 candidate" — and both G1 candidates that reached E-parts died mechanically today (M3 Phase-0 KILL; M5 confirmatory NO PASS — below). So even where a family can formally count 2-of-3 under the literal G3 wording, G3 cannot convert to GO because G1 fails independently; my per-family test is the substantive version the synthesis panel should weigh.

## 1. Family F1 — content personalization (user-lexicon ASR; the M3 family)

**(a) Verifiable reward: PASS.** WER / entity-WER, label-derived, committed machinery (`speechrl_common.rl.reward.wer`); exercised end-to-end in the C1 artifact (`_repro/asr_bon_llamacpp_snr5.json`: greedy 0.1183, oracle_red_8 +0.0418 [0.0289, 0.0564]).

**(b) Cross-session structure on available/buildable data: PASS at pseudo-session grade.** On-disk pseudo-sessions exist and were actually built with zero lockfile changes: LibriSpeech test-other chapters, same speaker reading the same book, rare entities recurring k≥3 (`_repro/m3_phase0_selection.json`: 36 utts / 13 train-960-freq-0 entities / 9 chapters; M3 lane file §"Minimal empirical prediction"). Caveats carried: real cross-session same-speaker audio does not exist publicly (D2 negative findings, r1 NOT MET as of 2026-07-03, 12 verified-empty searches), and external references warn the injection channel may be ignored even when supplied (D2-03 PROFASR-BENCH "context-utilization gap": oracle prompts produce little-to-no average WER change on Whisper/Qwen-Omni).

**(c) Demonstrated single-session cap: FAIL — the cap premise DIED.** M3 Phase-0 (`_repro/m3_phase0_zero_support.json`, commit 1b53b46): pooled entity-match fraction **F = 0.38108** vs frozen kill threshold **0.01** — 38x over, cluster-bootstrap CI [0.24477, 0.51823], consistent across 4 seed blocks (0.36111/0.40278/0.38194/0.37847), 439/1152 samples matched, greedy alone contains the entity in 38.9% of utterances, PILESER at 1.0. Artifact verdict verbatim: "M3 LANE KILLED (support already present in q0)". The information-availability premise is falsified at the model level: train-960h corpus rarity ≠ model-OOV (M3 lane file, E-part section) — the 30B's web pretraining already contains the book entities, so no single-session cap exists for lexical entities that a cross-session lexicon would lift. Residual observation, explicitly NOT a rescue (safeguard 8, kill-first ordering — no post-hoc extensions): genuinely unsupported entities exist but are the minority (SHARDURIS 0.0, CONFECTIONARY 0.0104, FARRINDER 0.0156 per-entity fractions in the same artifact); a re-scoped "true-OOV-only personalization" family would be a new pre-registration, not this campaign's evidence.

**F1 verdict: FAILS (a✓ b✓ c✗).** Also occupied-cell: the deliverable replicates deployed contextual biasing / phrase-hint products (M3 refuter, Occupied-cell check: Aleksic 2015, CLAS/Pundak 2018, Whisper hotword, Google/Amazon/Azure phrase lists) — zero GO novelty weight even if rebuilt.

## 2. Family F2 — accumulated-selector ASR (cross-session reward estimation; the M5 family)

**(a) Verifiable reward: PASS.** Same WER machinery; additionally the axis-(b) framing is coherent — deployment-time R is not reference-free computable (C1: mbr_sig false at N=1,2,4,8; D3-9: every published reference-free WER predictor is gradient-trained, hence out-of-fence; D3-2: model-internal confidence statistically null as a selector at G=16).

**(c) Demonstrated single-session cap: PASS — the cap is real and newly re-measured.** Single-shot label-free selection captures ~0–10% of oracle headroom: C1 dev pool mbr_red_8 = +0.0037 [−0.0082, +0.0170] n.s. vs oracle +0.0418 [0.0289, 0.0564] (`asr_bon_llamacpp_snr5.json`); on the fresh confirmatory slice MBR gains **nothing** over greedy (red_vs_greedy −0.00003, CI [−0.00358, +0.00369]) while oracle headroom is real (greedy 0.0772 → oracle@8 0.05342, +0.0238) — realized fraction −0.0008 (`_repro/m5_selector_confirmatory.json` summary; new post-7/02 measurement).

**(b) Cross-session structure on available/buildable data: FAIL on the strict reading (hollow), pseudo-session path exercised and exhausted.** The buildable path exists and was used — that is exactly why the ingredient now fails on evidence rather than on absence: (i) dev pool: ≤3/144 positions (2.1% upper bound) where any memory term could act; all 14 configs across 3 variant families tie MBR at exactly 0.0 (`_repro/m5_selector_dev.json`, structural_null_diagnostic); (ii) the **designed** deep-session surface — 12 speakers × 12 consecutive reading-order utterances, 3 replica seeds, 432 items, single touch — returned sel_wer_8 = mbr_wer_8 = shuf_wer_8 = **0.07722 exactly**; the memory selector never flipped a single MBR pick; per-position bins {1-4, 5-8, 9-12} all 0.000; ablation moot (gain_sel = gain_shuf = 0.0, load_bearing = False); artifact verdict verbatim: "PASS(i)=False PASS(ii)=False … Route: lane result stands as measured (no PASS)" (`_repro/m5_selector_confirmatory.json`). Threshold context: pre-registered PASS was ≥0.015 vs MBR with CI-LB>0 (prereg §5 M5); measured delta_vs_mbr = 0.0, CI [0.0, 0.0]. (iii) The only remaining surface class is a real cross-session corpus — r1 — which D2 verified does not exist publicly (D2 negative findings; nearest misses: AFA's PAT is synthetic dialogue text, D2-07; MSP-Podcast has undocumented session structure, license-gated, no SV-EER validation, D2-11).

**F2 verdict: FAILS on the strict reading (a✓ b✗-hollow c✓).** On the lenient/formal reading F2 counts 2-of-3 and is the only family to do so — but the prereg makes ambiguity resolve against GO (safeguard 1), and F2's own binding E-part is not ambiguous: it is a measured exact zero on the best surface buildable from frozen assets. Text-domain existence proofs (D2-08 VARS; D3-10; D3-11 — the last gradient-trained, out-of-fence) do not transfer GO-weight to speech under the novelty rule. The M5 refuter's G1 pincer also stands unanswered: any accumulated evidence that helped could be prompt-injected into the same frozen model, making the no-agency control non-null (route P-A, not GO) — but P-A's trigger (≥0.015, CI-LB>0) was itself not met ("P-A trigger NOT met", M5 lane file E-part status).

## 3. Family F3 — cross-session paralinguistics (the killed flagship)

**(a) Verifiable reward: FAIL.** S7 standing (prereg §8): measured-zero reward spread on the frozen content read-out (emotion NULL F6/NM3; speaker ~chance U4); by flat_no_gain a flat reward yields exactly zero gain at any session depth. New post-7/02 evidence points the same way: D3-6 (Züfle et al. 2026-05-27) — current speech QE metrics, including a SoTA SpeechLLM evaluator, are blind to speaker gender/prosody/emphasis and tend to ignore the audio signal; and the in-fence alternatives do not exist (D3-9: all reference-free WER/QE predictors are gradient-trained; purpose-built ECAPA/SER reward channels are S3-contingent unbuilt code — prereg §8 S3).

**(b) Cross-session structure: FAIL.** S1 standing/contingent: none of the 28 frozen datasets qualifies (CREMA-D acted, single-session — deep-review S1 via prereg §8). D2's r1 re-check is the decisive NEW evidence: **no public cross-session, same-speaker, multi-session speech corpus or benchmark appeared as of 2026-07-03** (12 verified-empty searches; the 2026 multimodal agent-memory benchmark wave — M3Exam D2-05, SMMBench/WorldMemArena D2-06 — uniformly excludes audio; mem0's own 07/02 industry report lists text-only memory benchmarks, D2-04). Buildable-in-principle via collection is S5 territory (multi-person, multi-month, annotation with IAA) — outside G4's ≤3-person-week bound by an order of magnitude.

**(c) Demonstrated single-session cap: FAIL (vacuously).** With zero measured spread there is no demonstrated headroom to cap; no committed artifact shows any single-session paralinguistic gain that cross-session structure could exceed.

**F3 verdict: FAILS 0/3 — unchanged from 7/02.** This is the family the deep review killed; nothing admissible today moves any ingredient.

## 4. Lane-suggested families (checked for completeness)

- **F4a — long-form context-carry ASR (M2 family).** (a) ✓ WER. (b) ✗ as a cross-session family: the structure is cross-BLOCK within one stream; on-disk substrate is concatenation pseudo-streams only (no long-form corpus in the frozen manifest — M2 refuter R3). (c) ✗ unmeasured: no SELF-conditioning arm exists in any committed artifact (M2 is DESIGN-ONLY; E-part post-GO per prereg §5) → inconclusive = NO-GO. Both blind refuters classify the mechanism as a single-model decoding flag occupied by Whisper/WhisperX (M2 lane, Occupied-cell check). Not a GO carrier.
- **F4b — segment-select-compose ASR (M4 family).** (a) ✓. (b) ✗ — no cross-session content at all (within-utterance granularity). (c) n/a — its real dev signal (K=3,N=8 oracle-granularity delta +0.0072 [0.0020, 0.0143]; seg-MBR +0.0029 [0.0005, 0.0058], dev-spent pool; M4 lane, Tier-1) is axis-(c) single-model material (P-C/P-D adjacency by the lane's own admission), and its deployable form inherits the F2 estimation null.
- **F4c — TTS pronunciation personalization (suggested by D2-01 FlowEdit: frozen flow-matching TTS + Hopfield memory, 92.7% relative PER reduction on 312 proper nouns, corrections persisting across sessions).** (a) partially — PER against a stored user correction is verifiable, but no TTS reward machinery is committed in-house; the S2-resolved operator was exercised in the ASR direction only. (b) buildable only via a new curated benchmark (the prereg's "TTS path"), i.e., lockfile expansion plus construction — nothing on disk. (c) ✗ not demonstrated on this stack, and the nearest in-house test of the analogous premise (corpus-rare ⇒ model-unsupported) just died at M3 Phase-0 (F=0.38108) — a Phase-0-style zero-support check would be mandatory and its prior is now adverse. A legitimate future candidate for a NEW pre-registration; carries zero GO-weight in this campaign (it is also a fast-follower signal on the A4-12 moat, D2-01/D2 negative findings).

## 5. Summary table

| Family | (a) reward | (b) cross-session data | (c) single-session cap | Passes all 3? |
|---|---|---|---|---|
| F1 content personalization | ✓ (WER/entity-WER; C1) | ✓ pseudo-session (m3_phase0_selection.json) | ✗ **died** — F=0.38108 vs 0.01 (m3_phase0_zero_support.json) | **NO** |
| F2 accumulated-selector ASR | ✓ (WER; C1) | ✗ hollow — ≤3/144 dev positions; 0 flips on designed surface (m5_selector_dev.json; m5_selector_confirmatory.json) | ✓ cap real — MBR ~0–10% of oracle headroom (C1; confirmatory −0.00003 vs oracle +0.0238) | **NO** (strict); 2/3 lenient, E-part null regardless |
| F3 cross-session paralinguistics | ✗ (S7; D3-6) | ✗ (S1; D2 r1 NOT MET) | ✗ (no measurable headroom) | **NO** (0/3) |
| F4a/b/c lane-suggested | ✓/✓/partial | ✗/✗/✗ | ✗-unmeasured/n-a/✗ | **NO** |

## 6. Pivot and re-open disposition from the B3 axis

- **P-A** (selector-learning-without-agency): trigger requires M5 E-part ≥0.015 with CI-LB>0 — measured 0.0; **NOT triggered** (committed in the artifact and lane file verbatim).
- **P-B** (benchmark-first): trigger requires "G3 fails only on the corpus ingredient." No family satisfies this: F1 fails on the cap (c), not corpus; F2's corpus path was exercised and the failure is empirical; F3 fails corpus AND reward AND cap. **NOT triggered from B3.** The one steelman — that F2's null is external-validity of pseudo-sessions vs real personalization streams (M5 lane, Open questions) — reduces to waiting on r1, which D2 verified unmet; that is a pre-registered re-open condition, not a pivot.
- **P-D** (condition-mapping) remains live as single-model Part-A material (Part-A memo verdict: RATIONAL-AND-CONTINUING; headroom real, +0.0418 [0.0289, 0.0564], hard-tail concentrated), but it is not a task-family GO and is outside B3's question.
- **Re-open-adjacent observations for the Decision Log** (not GO evidence): (i) the SHARDURIS/CONFECTIONARY residual shows a genuinely-unsupported entity minority exists — a future true-OOV personalization pre-registration would need model-level OOV screening, not corpus-frequency screening; (ii) r1 remains the binding unlock for F2 and F3 alike; (iii) the F2 collateral finding (deployable label-free capture ≈ 0% of a real +0.0238 oracle headroom on a fresh slice) sharpens the single-model estimation-gap problem that P-A-class work would target under its own future trigger.

## 7. Verdict

**No task family passes the three-ingredient test.** The only new-information items admissible for GO-weight under safeguard 4 — the M3 Phase-0 artifact, the M5 dev+confirmatory artifacts, the D2 r1 re-check, and the new C1-artifact analyses — all load on the NO-GO side of the ingredients question. B3 therefore supports the standing 2026-07-02 null: the agent-level framing has no task family in which verifiable reward, cross-session data, and a demonstrated single-session cap coexist, and the two families whose pilots ran (F1, F2) each lost their load-bearing ingredient by pre-registered mechanical measurement (F=0.38108 vs 0.01; delta_vs_mbr = 0.0 vs ≥0.015).

---

## B4 — VoI / named-decision check (applies frozen criterion G2; answers objection U2)

**Verdict:** G2 SATISFIED-IN-FORM BUT CANNOT CARRY GO — named >=2-action decisions exist (D-1..D-4 below) and demonstrably changed when the pre-registered experiments ran (M3 Phase-1 cancelled; V4 selector-memory build killed); recommended ledger disposition: U2 ANSWERED for the reduced selector-memory scope, U2 STANDS for the full omni-agentic system absent r1. G1 failed mechanically (M3 killed at F=0.38108 vs 0.01; M5 confirmatory no-pass at delta=0.0), so B4 concurs NO-GO. Error-cost asymmetry (wrong-GO ~5-7 person-weeks sunk + quarter of GPU + repeat-collapse risk vs wrong-NO-GO bounded, reversible via r1-r3) vindicates the frozen inconclusive=NO-GO rule. Step-2 kill criteria K1-K6 pre-registered, including what kills the omni-agentic-survey product itself.

# B4 lane memo — VoI / named-decision check (G2; objection U2)

> Step-1 rationality campaign · 2026-07-03 · pre-registration freeze b19bff2 · role: B4 analyst.
> Null hypothesis: the 2026-07-02 NO-GO verdict (deep-review.md). Inconclusive = NO-GO.
> Role-separation note (safeguard 10): B4 *recommends* ledger dispositions; the Phase-5 panel adjudicates ANSWERS vs ROUTES-AROUND.

## 1. Lane statement

B4 is not a mechanism lane; it carries no B0 axis claim (B0 gates GO-supporting *mechanism* arguments, prereg §1). B4 applies frozen criterion **G2** (prereg §2): "A NAMED downstream decision that changes depending on the answer, plus pre-registered kill criteria for step 2. No named decision → U2 stands → no GO." Every GO-weighted item below is post-7/02 evidence per safeguard 4: the two new pilot artifacts (`_repro/m3_phase0_zero_support.json`, `_repro/m5_selector_confirmatory.json`), the dev grid (`_repro/m5_selector_dev.json`), and delta-scan claims (D1-*, D2-*, D3-*).

## 2. The named decision — answering U2 head-on

U2 (prereg §8, quoting deep-review.md:34-35): "VoI ≈ 0: no decision changes regardless of which way the central question resolves; the claimed novelty is 'an empty cell in a design matrix'." Its frozen overturn condition: *a concrete decision with real cost stakes where the pre-registered agentic arm beating **(or losing to)** the strongest single-model baseline changes what gets built, demonstrated by actually running that decision-relevant experiment* (prereg §8, U2 row).

I can name the decision. It is a four-row, next-quarter, this-project allocation matrix, each row with ≥2 distinct actions:

| id | decision | GO / GO-minimal action (next quarter) | NO-GO action (next quarter) |
|----|----------|----------------------------------------|------------------------------|
| **D-1** | **Selector work on the C1 gap** — W1's committed roadmap item "close the realized-vs-headroom gap (a stronger label-free selector)" (wiki/Per-Work-Status.md, W1 section) | Build and ship the **session-memory selector (V4-class) in the W1 selector stack** for personalization-style ASR vs MBR alone — the decision named verbatim in the M5 lane (mechanism-selector-accumulation.md, Constructor case §(5)); ≤3 person-weeks per G4 (prereg §2) | **Do not build.** Kill the memory-selector family; re-scope the C1-gap thread to the untried single-shot in-fence families: per-token logprob self-certainty rescoring (the S6 residual, prereg §8 note 5; D3-1), frozen-judge rescoring (part-a-memo.md §A2), and P-D condition-mapping (prereg §2) |
| **D-2** | **WF-2 scope** — the next workflow the prereg gates behind the owner ("Owner gate before any publication and before WF-2", prereg §7) | WF-2 = the scoped build campaign per the B.1 GO skeleton (prereg §9.1); the omni-agentic survey doubles as the build's design document | WF-2 does not launch as a build. Any survey product re-scopes from "the system we will build" to "the question is closed; re-open conditions r1–r3" — the citable closure for the converged paper's deferred-not-disproved future-work sentence (prereg §9.2 item 6) |
| **D-3** | **Corpus building** (S1 / P-B / r1) | Initiate the lockfile-regeneration corpus path: MSP-Podcast academic-license application + cross-session metadata + SV-EER admission-band validation (D2-11; prereg §8 note 1), and/or a TTS pseudo-session pipeline (prereg §2 G3) | No lockfile unlock, no license application, no pipeline. Standing r1 monitor only (periodically re-run the D2 negative-finding searches, which verified r1 NOT MET across 12 searches on 2026-07-03) |
| **D-4** | **W4 post-NULL queue priority** | W4's queue yields ~a quarter of the single 24 GB 5090's capacity to the agent build | W4 queue proceeds immediately: same-audio SSL baseline, multi-vector/trajectory emotion readout, emotion2vec fusion, W1→W4 RL-on-speaker bridge, then content/language fan-out (wiki/Per-Work-Status.md, W4 "Next") |

So the direct answer to "if you cannot name a real decision, say so": **I can, and it is not hypothetical — two of the four rows already resolved this week, by measurement.**

## 3. The behavioral proof that VoI > 0: the decision-relevant experiments actually ran

U2's overturn clause demands the experiment be *actually run*, with the "(or losing to)" branch explicitly admissible. Both pre-registered pilots ran post-freeze and both fired the losing branch, and the build queue changed accordingly:

- **D-1 resolved to NO-BUILD by `_repro/m5_selector_confirmatory.json`** (single touch, 144 fresh utts × 3 replica seeds = 432 items; ~3,888 llama.cpp generations, ~8–16 h wall-clock per the M5 lane cost line): `sel_wer_8 = mbr_wer_8 = 0.07722` exactly — zero flips; `delta_vs_mbr = 0.0`, CI [0.0, 0.0]; `red_vs_greedy = −0.00003`, CI [−0.00358, +0.00369]; threshold 0.015 → `PASS=false` on both readings; ablation moot (`gain_sel = gain_shuf = 0.0`); P-A trigger NOT met. Collateral finding with independent decision force: MBR itself gains *nothing* over greedy on the fresh slice while oracle headroom is real (0.0772 → 0.05342, +0.0238) — deployable label-free capture ≈ 0%.
- **M3 Phase-1 resolved to CANCEL by `_repro/m3_phase0_zero_support.json`**: pooled entity-match F = **0.38108** vs kill threshold 0.01 (38× over; cluster-bootstrap CI [0.245, 0.518]; 1,152 samples; consistent 0.36–0.40 across 4 seed blocks; greedy alone contains the entity 38.9% of the time). This cancels the pre-costed Phase-1 four-arm pilot (~2,850 generations, 5–8 h per the M3 lane cost estimate) and removes user-lexicon memory injection from the W1 roadmap.

Before these runs, the Part-A memo (§A3) recorded the coupling in writing: "A named decision hinges on the result — VoI > 0 by construction." GPU-hours were spent contingent on outcomes and the outcomes stopped planned work. That is decision-value demonstrated behaviorally — the exact thing U2 said did not exist.

## 4. The honest split — where U2 stands anyway

- **Reduced scope (selector-memory agent, GO-minimal grade): recommend U2 = ANSWERED.** The named decision existed with cost stakes (G4-scoped build), the pre-registered agentic arm was run against the strongest single-model label-free baseline (MBR), it lost, and what gets built changed. U2's own overturn text is satisfied in its "(or losing to)" branch.
- **Full omni-agentic system (routing + skills + cross-session paralinguistics): U2 STANDS.** No next-quarter action differs by verdict at that scope, because S1 (corpus, contingent), S3 (stack unbuilt, contingent) and S5 (resources, contingent) block any full-system build under *either* verdict (prereg §8 + resolution notes 1/3/4); M2/M4 were design-only lanes whose refuters both recommend "likely-dies" with no build decision attached. Absent r1, that design-matrix cell contains no decision with cost stakes — the prosecution is right there, and the GO-minimal grade existed precisely "to stop a bounded agency role from being inflated into the full system" (prereg §2). The M5 refuter's occupied-cell finding ("U2's empty cell is not even empty" — biasing/QE/MBR prior art) further caps any novelty claim at that scope.

This split cannot rescue GO: G2 is a conjunct, and **G1 failed mechanically** (M3 killed; M5 no-pass; M2/M4 no E-parts by design). B4 concurs **NO-GO**.

## 5. Asymmetric error costs (B5-style)

**Wrong-GO (build on a false mechanism) — sunk, front-loaded:**
- Minimal build: ≤3 person-weeks (G4 cap, prereg §2), realistically the full cap given the M5 lane's instrument-design churn (frozen V1 was provably 3 orders of magnitude too weak — median flip-λ 60.5 vs frozen 0.05, M5 lane A7).
- Pilot compute: Phase-1 ~5–8 h + ≥2 confirmatory-class runs at 8–16 h each ≈ **20–40 GPU-h** on the only GPU (M3/M5 lane cost lines) — $0 marginal but ~a quarter of the single-24 GB-5090 queue (D-4 stalls the W4 flagship's four named next steps).
- Corpus path if triggered: full version "multi-person, multi-month" (prereg §8 S5); minimal MSP-Podcast validation + TTS pseudo-sessions ≈ **2–4 person-weeks** (B4 estimate, flagged as estimate).
- Tail risk: a second adversarial collapse — the documented precedent (deep-review.md header; Per-Work-Status cross-work section) consumed 4 hostile review rounds + a POMDP restructure + a full paper reframing.
- Posterior context: every measured agentic number is 0.0 (`m5_selector_dev.json` all-14-configs zero; `m5_selector_confirmatory.json` zero), the M3 premise is falsified 38× (`m3_phase0_zero_support.json`), and 92% of residual headroom sits on anti-consensus minority-best pools (M5 lane, refuter R3(3)). **Estimated total wrong-GO cost: ~5–7 person-weeks sunk + a quarter of GPU/attention + repeat-collapse exposure.**

**Wrong-NO-GO (walk away from a real mechanism) — bounded, reversible:**
- The loss is first-mover position on the open moat: speech-native cross-session memory/skills (archive claim A4-12, re-verified OPEN on 2026-07-03 by the D2 negative findings) and M5's exact cell (no published no-gradient accumulating ASR selector; D3 negative findings: "no scoop risk for M5").
- The fast-follower clock is visibly running: FlowEdit (D2-01, 2026-06-18) — frozen-model speech lifelong memory in TTS, 92.7% relative PER reduction; AFA (D2-07) — speaker-keyed per-user memory stores, 35.7%→61.3% persona attribution; the May–June 2026 multimodal-memory benchmark wave is one modality from speech (D2-05, D2-06); mem0 ships three voice integrations with no voice-memory benchmark (D2-04). Realistic window: **2–4 quarters**.
- But the loss is capped three ways: (i) **reversibility** — r1–r3 re-open conditions are pre-registered with ~zero monitoring cost (prereg §2); (ii) **the benchmark half of the moat is not closed by NO-GO** — P-B remains a named pivot (prereg §2), so the buildable asset (a cross-session speech-memory benchmark) survives the mechanism verdict; (iii) **probability** — the mechanism's measured effect is exactly 0.0 twice on designed surfaces, so P(real | data) is low.

**Conclusion:** wrong-GO is sunk with a documented catastrophic precedent; wrong-NO-GO is bounded and recoverable. The frozen "inconclusive = NO-GO" rule (prereg §6.1) is decision-theoretically correct for this cost structure, not merely conservative.

## 6. Pre-registered step-2 kill criteria (including what kills the omni-agentic-survey product itself)

- **K1 — occupied-cell kill (survey product).** The survey ships only if the D2/D3 negative-finding searches, re-run ≤2 weeks before submission, still show the cell unoccupied. A published speech-native cross-session memory benchmark or no-gradient accumulating speech selector kills the "open moat / first" framing → descope to review-only with the fast-follower caveat (safeguard 9).
- **K2 — recursive no-decision kill (survey product).** If at submission the survey cannot bind each surveyed cell to a named build/no-build decision in W1–W4 (this memo's own test applied recursively), the product is killed by U2's standard. The M5 refuter's occupied-cell evidence (biasing/QE/MBR literatures) is the bar any residual-novelty claim must clear.
- **K3 — corpus-admission kill (P-B).** No corpus passing the SV-EER admission band within one quarter of the license/TTS path starting → kill (prereg §8 note 1).
- **K4 — budget kill.** >3 person-weeks or does not run on the 24 GB 5090 → kill (G4 carried forward).
- **K5 — Goodhart kill.** Proxy improves while true WER degrades on any arm → kill regardless of proxy score (prereg §5 M5 guard, carried forward).
- **K6 — headroom-floor kill (kills the C1-gap thread itself, agentic or not).** If P-D condition-mapping shows clean-audio oracle headroom CI-UB < +0.01 WER at N=8, the selector-gap program loses its target entirely (modeled on M2's pre-registered kill line, prereg §5).

## 7. B4 verdict

**G2 is satisfied in form — the named decisions existed, with GPU receipts — and that satisfaction is exactly why the NO-GO is citable rather than apathetic.** The strongest available answer to U2's closing jab ("the authors concede the system is 'not worth building now'") is that this campaign converted the concession from opinion to measurement: the decision-relevant experiments were pre-registered, run once, and resolved the build decision to NO-BUILD (D-1, D-2) while releasing the freed capacity to named successors (D-4 W4 queue; D-1 single-shot selector families; D-3 r1 monitor). Recommended ledger disposition for the Phase-5 panel: **U2 ANSWERED for the reduced selector-memory scope; U2 STANDS for the full omni-agentic system absent r1.** Since G1 failed mechanically on both executed lanes, G2 cannot move the verdict: **B4 concurs NO-GO**, with the decision matrix of §2 and the kill criteria of §6 entering the NO-GO decision doc as items 3 and 5 of the B.2 skeleton.

### Evidence index
- Prereg: `wiki/2026-07-03-agentic-tfrl-step1-preregistration.md` @ b19bff2 (§1 B0; §2 G1–G4/GO-minimal/P-A–P-D/r1–r3; §5 M3/M5/M2 thresholds; §6 safeguards; §7 WF-2 owner gate; §8 U2 row + S1/S5 notes; §9 skeletons).
- Artifacts: `projects/speech-mllm-training-free-rl/_repro/m3_phase0_zero_support.json` (F=0.38108, CI [0.245, 0.518], kill 0.01, n=1,152, KILL=true); `_repro/m5_selector_dev.json` (14 configs all-zero; winner V1|0.05|none; ≤3/144 actionable positions); `_repro/m5_selector_confirmatory.json` (sel=mbr=0.07722; delta 0.0 CI [0,0]; oracle 0.05342; MBR-vs-greedy −0.00003 CI [−0.00358, +0.00369]; PASS=false ×2; ablation moot); `_repro/asr_bon_llamacpp_snr5.json` (oracle +0.0418 [0.0289, 0.0564] @ N=8; MBR +0.0037 [−0.0082, 0.017] n.s.).
- Lane files: D3-1, D3 negative findings ("M5's exact object is unoccupied… no scoop risk"); D2-01, D2-04, D2-05, D2-06, D2-07, D2-11, D2 negative findings (r1 NOT MET; A4-12 open); M3 lane (cost_estimate; E-part KILLED); M5 lane (B0 statement; Constructor case §(5) named decision; A7 λ-census; refuter R3(3) 92% anti-consensus; cost_estimate; E-part NO PASS); Part-A memo §A2/§A3.
- Prosecution source: `papers/agent-level-tfrl/reviews/deep-review.md` lines 33–35 (U2), header (collapse precedent).
- Status board: `wiki/Per-Work-Status.md` (W1 roadmap; W4 "Next" queue; cross-work paper section).

---

## B5 — feasibility / minimal-build costing (G4 gate: ≤3 person-weeks, single 24 GB RTX 5090, no licensing/consent blockers)

**Verdict:** ALL THREE MINIMAL BUILDS FIT G4 ON COST AND COMPUTE — BUT NONE OF THEIR FROZEN TRIGGERS FIRED TODAY. GO-minimal (~1–1.5 pw) is buildable yet untriggered: the binding M5 confirmatory artifact reads NO PASS with gain_sel = gain_shuf = 0.00000 and ablation moot (_repro/m5_selector_confirmatory.json, summary.verdict). P-A (~1–2 pw) is the cheapest build — the re-scoring infra is already committed — but its own trigger (≥0.015 vs MBR, CI-LB>0 on the fresh slice) measured 0.0 exactly. P-B splits in two: a pseudo-session/TTS entity-memory benchmark fits the budget (~1.5–2.5 pw) but does NOT satisfy r1/S1 (synthetic precedent D2-07); a genuine S1-satisfying paralinguistic corpus exceeds G4 (license acquisition + SV-EER validation + affect verification, plus biometric-consent friction) and r1 is verified unmet as of 2026-07-03 (D2 negative findings). S1: contingent, UNMET. S3: contingent, materially NARROWED for the selector-memory slice only (committed code c8bebaf/d4dd117/1b53b46/f8ec1d3). S5: in-budget only for the three scoped routes; full-program resources still multi-person/multi-month. Feasibility is therefore not the binding constraint anywhere — the frozen E-part evidence is. Per the pre-registration (inconclusive = NO-GO), B5 supplies no GO-weight; it only certifies that IF the synthesis panel routes to a pivot, the pivot builds are cheap and unblocked (P-A cheapest, P-B tier-1 next, GO-minimal buildable but criterion-dead absent an owner-signed amendment).

# B5 feasibility memo — minimal-build costing for the surviving routes

Role: B5 feasibility analyst. Binding criteria: pre-registration `wiki/2026-07-03-agentic-tfrl-step1-preregistration.md` @ freeze b19bff2 — G4 (≤3 person-weeks, single 24 GB RTX 5090 Laptop GPU, no licensing/consent blockers), scope fence §3 (gradient-trained selectors OUT), null hypothesis = the 2026-07-02 NO-GO, inconclusive = NO-GO. All numbers below trace to committed artifacts, committed scripts, or lane-file evidence IDs. Person-week (pw) figures are B5 estimates grounded in measured wall-clock times and the committed code inventory; they are the only non-artifact numbers and are labeled as such.

## 0. Trigger-status preamble (honesty gate before any costing)

B5 costs builds; it does not grant triggers. As of today's binding artifacts, **no route's frozen trigger has fired**:

- **GO-minimal trigger (prereg §2): NOT MET.** Requires M5 PASS + shuffled-memory ablation load-bearing. The binding E-part `_repro/m5_selector_confirmatory.json` `summary.verdict` reads: "PASS(i)=False PASS(ii)=False agree=True; gain_sel=+0.00000 gain_shuf=+0.00000 load_bearing(<=50% retained)=False; goodhart_fail=False. Route: lane result stands as measured (no PASS)." sel_wer_8 = mbr_wer_8 = 0.07722 exactly — zero flips on the designed 12-speaker × 12-consecutive-utterance surface (commit f8ec1d3).
- **P-A trigger (prereg §2): NOT MET.** Requires realized reduction ≥0.015 vs MBR, CI-LB>0, on the fresh confirmatory slice. Measured: delta_vs_mbr_mean = 0.0, CI [0.0, 0.0] (`m5_selector_confirmatory.json` summary.primary). The M5 lane file records "P-A trigger NOT met" verbatim (lane §E-part status).
- **P-B trigger (prereg §2): NOT MET AS STATED.** Requires "G3 fails ONLY on the corpus ingredient." Today G3's theorem ingredient is also dead: M3 killed at Phase-0 (F = 0.38108 vs kill threshold 0.01, 38× over, CI [0.245, 0.518]; `_repro/m3_phase0_zero_support.json`, commit 1b53b46) and M5 recorded NO PASS — so no G1 candidate survives, and G3 fails on two ingredients (corpus + theorem), not one. Only the operator ingredient stands (S2 resolved; prereg §8 note 2).

Costing below proceeds as tasked, because B5's output is an input to the synthesis panel regardless of trigger state (it prices the pivots and certifies/denies G4).

## 1. GO-minimal — selector-memory agent (index + verifiable-reward acceptance gate over the existing llama.cpp operator)

**Scope (per tasking):** exactly the reduced object — a retrieval index over harvested session tokens plus a verifiable-reward admission gate, layered on the existing frozen-Qwen3-Omni llama.cpp best-of-N operator. Explicitly NOT the S3 full stack (no ECAPA, PLDA, AS-Norm, pyannote, CUSUM, BOCPD, SER head, memory graph, skill library).

**What already exists (committed, artifact-emitting):**
- Operator: `scripts/repro_asr_best_of_n_llamacpp.py` + resident llama-server (`-ngl 28`, Q8_0 GGUF) — commits b7b4b0d / cd6aa92 / f9d111a; anchor artifact `_repro/asr_bon_llamacpp_snr5.json` (oracle +0.0418 [0.0289, 0.0564] @ N=8, n=144, 3 gen seeds).
- Memory-selector machinery: `scripts/m5_selector_rescore_dev.py` (CPU-only, deterministic re-scoring of committed pools; reproduce line in `_repro/m5_selector_dev.json`) and `scripts/m5_selector_confirmatory.py` (five arms: greedy / MBR / frozen selector / shuffled-memory / oracle; session state per replica; speaker-rotation-derangement shuffle control; cluster bootstrap 10k draws; Goodhart true-WER-by-N guard) — commits d4dd117 (freeze before generation) and f8ec1d3 (verdict).
- Gate options: the dev grid already swept 14 configs across three variant families with gate parameters (`_repro/m5_selector_dev.json` grid: V1 ×8, V2 ×3, V3 ×3; winner V1|0.05|none by frozen tie-break).

**Marginal build (B5 estimate):**
| item | basis | cost |
|---|---|---|
| Index module (rare-token store keyed by session/speaker, harvest from pools) | refactor of logic already inside the dev/confirmatory scripts | 2–3 days |
| Verifiable-reward acceptance gate (consensus-m / MBR-agreement admission) | gate hooks already in the dev grid | 1–2 days |
| Session runner + arms + stats | reuse `m5_selector_confirmatory.py` nearly verbatim | ~1 day |
| One fresh confirmatory slice (144 utts × 3 replicas × 9 generations = 3,888 llama.cpp calls) | measured elapsed_s = 25,988 (~7.2 h wall) on the single 5090; M3 Phase-0 (1,188 samples) took 1,886 s | ~1 GPU-day incl. staging |
| **Total** | | **~1–1.5 pw, well under 3 pw; 24 GB fit demonstrated, $0 marginal** |

**G4 verdict for GO-minimal: PASS on cost/compute/licensing — but criterion-dead as frozen.** The identical minimal object was already built and measured: on the designed deep-session surface it never flipped a single MBR pick (sel == MBR == 0.07722), MBR itself gained nothing over greedy (−0.00003, CI [−0.0036, +0.0037]) while real oracle headroom (+0.0238) went 0% captured (`m5_selector_confirmatory.json` summary.arms, realized_fraction ≈ −0.0008). Any re-build would have to use a different functional form (the constructor's V4 memory-dominant selector, dev-only evidence: +0.00611 LOO / +0.00321 streaming vs MBR, CIs crossing 0 — M5 lane §Minimal empirical prediction), which requires an owner-signed amendment under the freeze (prereg header + safeguard 5); its own constructor predicts sub-threshold results on entity-unselected slices (+0.001 to +0.006, "CI likely crossing 0"). Cheap ≠ warranted: buildable, untriggered.

**Licensing/consent:** clean as scoped. LibriSpeech is CC BY 4.0 (LibriVox-derived); memory state is text-only (harvested token strings keyed by dataset-supplied speaker labels), no voice-embedding extraction, no enrollment of real users — no biometric processing. See §5 for the boundary that must not be crossed without new consent machinery.

## 2. P-B — benchmark-first (pseudo-session / TTS corpus construction + planned lockfile expansion)

Two tiers with opposite G4 outcomes; the synthesis panel should not let tier-1's feasibility be quietly traded for tier-2's claim.

**Tier 1 — pseudo-session / TTS entity-memory benchmark (ASR-lexicon axis): IN BUDGET (~1.5–2.5 pw), but does NOT satisfy r1/S1.**
- Construction machinery exists and has run twice: deterministic entity/pseudo-session selection `scripts/m3_phase0_select_entities.py` → `_repro/m3_phase0_selection.json` (36 utts, 13 train-960-freq-0 entities, 9 chapters, commit c8bebaf); the 12×12 consecutive reading-order slice `_repro/m5_confirmatory_slice_ids.json` (seed 20260703, dev-spent exclusions). Generalizing to a releasable benchmark (manifest + baselines + admission stats + docs): ~1–2 pw (B5 estimate). Zero new data, zero lockfile change.
- TTS variant (synthetic multi-session same-speaker audio with controlled entity recurrence): local TTS fits 24 GB; ~1–2 pw (B5 estimate). Consent-clean if stock/synthetic voices are used (cloning a real person's voice requires speaker consent).
- **Hard cap on what tier 1 proves:** the prereg's own r1 re-open condition demands a PUBLIC cross-session same-speaker corpus, and the campaign's own precedent (D2-07: AFA's synthetic PAT dataset "does not satisfy r1/S1") rules synthetic/pseudo data out for S1. Validity risks are also on record: pseudo-session recurrence structure just produced two adverse results in-house (M3 KILL; M5 NO PASS), the M5 lane itself flags "LibriSpeech chapter reading is a weak proxy for real cross-session personalization streams" (lane §Open questions), and PROFASR-BENCH (D2-03) shows frozen models under-utilize injected context even with ORACLE prompts — direct risk evidence against the benchmark's headline contrast being non-degenerate.
- VoI context (for the panel, not GO-weight): the cell is genuinely open — mem0's 2026-07-02 industry report ships three voice integrations with zero voice-memory benchmark (D2-04); the entire May–June 2026 multimodal-memory benchmark wave excludes audio (D2-05, D2-06); IndicContextEval (D2-02) provides a ready seven-level injection/adversarial template. But the near-neighbor cell (context-conditioned ASR benchmark) is already occupied by PROFASR-BENCH (D2-03) — the unoccupied sliver is specifically cross-session memory.

**Tier 2 — genuine S1-satisfying corpus via lockfile expansion: EXCEEDS G4.**
- The expansion route itself is legitimate policy (prereg P-B: "the dataset freeze is POLICY, not physics") and the machinery exists (`scripts/data/fetch-data.sh` + `scripts/data/gen-lockfile.py`, per CLAUDE.md).
- Nearest candidate: MSP-Podcast (D2-11) — 400+ h naturalistic, emotion-annotated (≥5 raters), speaker-ID'd. But: same-speaker cross-session structure is UNDOCUMENTED in both the paper and the lab distribution page; access is an institution-signed academic license (weeks of admin latency, likely non-redistributable — a benchmark built on it could release protocol/metadata only, not audio); and no SV-EER admission-band validation exists. Post-acquisition validation (pretrained SpeechBrain ECAPA for SV-EER, trivially within 24 GB, ~0.5 pw) is cheap, but the S1 resolution note additionally demands verified affect variation across temporally separated sessions — human verification effort on top. Aggregate: license acquisition + session-structure forensics + SV-EER band + affect validation > 3 pw even before the corpus risk (it may simply lack the structure), and the whole path processes real speakers' biometric-adjacent data (§5).
- r1 status: verified UNMET as of 2026-07-03 — 12 targeted searches found no public cross-session same-speaker speech corpus or benchmark; no spoken/TTS variant of LoCoMo/LongMemEval exists (D2 negative findings).

**G4 verdict for P-B: split.** Tier 1 PASSES G4 but cannot discharge S1 and carries measured degeneracy risk; tier 2 would discharge S1 but FAILS G4 (person-weeks + license latency + consent friction). Note also that P-B's own trigger precondition ("G3 fails only on corpus") is not the world we are in (§0).

## 3. P-A — selector-learning-without-agency (closing the C1 realized-vs-headroom gap)

**Infra: already built and committed — the cheapest route on the board.**
- Re-scoring loop: `scripts/m5_selector_rescore_dev.py` — reproduce line (from `_repro/m5_selector_dev.json`): "SPEECHRL_DATA_DIR=<repo>/speechrl-data python scripts/m5_selector_rescore_dev.py (CPU-only; re-scores the committed C1 pools; deterministic)". Dev iterations cost ~minutes of CPU, zero GPU (M5 lane cost_estimate: "Tier-0 … ~4 min total, zero GPU").
- Confirmatory harness with dev/test hygiene, arms, cluster bootstrap, and Goodhart guard: `scripts/m5_selector_confirmatory.py` (commits d4dd117/f8ec1d3). Fresh-slice generation cost measured: 25,988 s ≈ 7.2 h per 144-utt × 3-replica slice.
- Candidate pools to learn against: `_repro/asr_bon_llamacpp_snr5.json` (dev-spent, 144 utts × 9 generations) + the confirmatory pools now equally spent — new confirmatory claims need fresh slices, one touch each (prereg §4).

**The target is real and quantified:** oracle +0.0418 [0.0289, 0.0564] @ N=8 vs MBR +0.0037 n.s. (~9–10% of headroom) on C1; on the confirmatory slice deployable capture was ~0% of a +0.0238 headroom. Named in-scope, untried selector families (Part-A memo A2): (i) frozen-model per-token-logprob self-confidence — blocked on the S6 residual (interface never exercised; prereg §8 note 5); (ii) frozen-judge rescoring (second frozen model, no gradients); (iii) external frozen-LM MBR utility — D3-2 shows RoBERTa-PLL utility recovering 9.0% relative WER (p<0.0001) where internal confidence is statistically exhausted, and D3-10 shows sampling-consistency confidence working as a training-free selection signal in retrieval settings. D3-9's negative finding (every published reference-free WER predictor is gradient-trained) confirms nothing can be adopted off-the-shelf — the fence-compliant families above are the whole search space.

**Marginal cost (B5 estimate):** S6-residual logprob verification ~1–2 days; two to three new selector families as CPU re-scorers over committed pools ~3–5 days; one fresh confirmatory slice ~1 GPU-day. **Total ~1–2 pw.** G4: PASS with margin.

**Honesty item:** P-A's pivot trigger did not fire (§0) — the confirmatory delta vs MBR was 0.0 exactly, and the refuter's C1 decomposition (M5 lane R3) shows 92% of residual headroom sits on ≤2-of-8 minority candidates, i.e., structurally anti-consensus for majority-seeking label-free signals. P-A is cheap to attempt and correctly scoped as a single-model paper (no agentic claim), but B5 flags that its measured base rate to date is: every deployable selector null.

## 4. S1 / S3 / S5 status with today's evidence

| item | 7/02 status | today | evidence |
|---|---|---|---|
| **S1 (corpus)** | contingent (data) | **contingent, UNMET; no state change.** r1 verified not met 2026-07-03 (12 empty searches); nearest candidate MSP-Podcast license-gated with undocumented session structure; synthetic/TTS explicitly non-qualifying (AFA precedent). | D2 negative findings; D2-11; D2-07 |
| **S3 (unbuilt stack)** | contingent (engineering) | **contingent, materially NARROWED on one slice only.** The "nonexistent code vs nonexistent code" charge no longer holds for the selector-memory slice: committed, artifact-emitting implementations of the operator, memory selector, shuffled control, and confirmatory harness now exist and have completed end-to-end runs (the S3 resolution condition's letter, for this slice). The full ECAPA/PLDA/AS-Norm/pyannote/CUSUM/BOCPD/SER/memory-graph/skill-library stack remains unwritten — and GO-minimal as scoped deliberately never needs it. | commits c8bebaf, d4dd117, 1b53b46, f8ec1d3; `_repro/m3_phase0_zero_support.json`, `_repro/m5_selector_dev.json`, `_repro/m5_selector_confirmatory.json`; deep-review.md lines 52–53 |
| **S5 (resources)** | contingent (resources) | **contingent for the full program; DISCHARGED within scope for the three routes costed here.** All measured runs completed on the single 24 GB 5090 (llama-server `-ngl 28`; 7.2 h confirmatory; 0.5 h M3 Phase-0; CPU-only dev re-scoring); zero human annotation used. The full-program clause (human SER annotation + spontaneous corpus + full stack = multi-person/multi-month) stands untouched and is exactly what makes P-B tier 2 fail G4. | artifact `elapsed_s` fields (25,988 / 1,886); M5 lane cost_estimate; deep-review.md lines 54–57 |

## 5. Licensing / consent notes (voiceprints = biometric)

1. **Data & model, as-scoped routes:** LibriSpeech CC BY 4.0 — redistribution and derivative benchmarks fine with attribution. Qwen3-Omni-30B-A3B GGUF: Apache-2.0 per the Qwen3 model-card family — local inference and published numbers unencumbered (verify the specific GGUF repack's card before any redistribution of weights). No blocker for GO-minimal, P-A, or P-B tier 1.
2. **The biometric boundary.** Voiceprints and speaker embeddings are biometric identifiers: GDPR Art. 9 special-category data (explicit consent), Illinois BIPA (private right of action, statutory damages), and — directly relevant to this team's jurisdiction — China PIPL sensitive-personal-information rules (separate consent + necessity assessment). The costed GO-minimal/P-A builds stay on the safe side **only because** memory is text-only and keyed by dataset-published speaker labels of consented public read speech; no ECAPA/x-vector extraction on real users, no enrollment. Any drift toward speaker-keyed memory via voice embeddings (the AFA/D2-07 pattern, or the deferred program's ECAPA+PLDA arms) crosses into biometric processing and voids the "no consent blockers" clause of G4 until a consent instrument exists.
3. **P-B tier 2 specifics:** MSP-Podcast is served under an institution-signed academic license (D2-11) — audio non-redistributable, so a benchmark built on it can release only protocol/metadata/splits; collecting a NEW spontaneous multi-session corpus means recording identifiable voices across sessions = biometric collection requiring consent forms and plausibly IRB-grade review — a legal/admin cost outside the 3-pw envelope independent of compute. TTS-corpus construction: voice cloning of real speakers requires the speaker's consent and is restricted by most TTS model licenses; stock synthetic voices avoid this at the price of S1-validity (which is already zero per D2-07).

## 6. Bottom line for the synthesis panel

Feasibility is nowhere the binding constraint — evidence is. All three minimal builds fit G4 on cost and compute (GO-minimal ~1–1.5 pw; P-A ~1–2 pw; P-B tier 1 ~1.5–2.5 pw; all demonstrated or trivially projected on the single 24 GB GPU; licensing clean as scoped). But B5 can supply no GO-weight: the GO-minimal and P-A triggers measured exact zeros on the binding confirmatory artifact, P-B's trigger precondition fails on two ingredients rather than one, S1 is unmet, and the only S-item that moved (S3, narrowed on the selector-memory slice) moved by producing the very null artifacts that kill the triggers. Under the frozen rule — inconclusive = NO-GO — the feasibility lane's contribution is: IF the panel routes to a pivot as a recorded success, P-A is the cheapest and fully unblocked, P-B tier 1 is affordable but cannot claim S1/r1, and GO-minimal, while buildable in a week and a half, has no criterion left to authorize it absent an owner-signed amendment plus fresh evidence.

---
