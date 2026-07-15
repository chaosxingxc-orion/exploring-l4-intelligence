# Stage-1 3W cross-domain comparisons (WHY / HOW / WHAT + transfer verdicts)

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).



---

# 3W: self-refine/self-correction (text vs VLM vs speech-GER)

# 3W Comparison — Self-Refine / Self-Correction: text-LLM vs VLM vs speech (GER/HyPoradise-class)

**Method:** ars-3w (WHY/HOW/WHAT + transfer verdict) · **Date:** 2026-07-04 · **Frame:** mapped onto the sufficiency-yardstick memo (H_fix / H_prompt / ρ; conditions a, b1, b2, c) · **Verification:** all 10 sources below resolved to real pages this session; per-claim tags: `fence`, `ladder`, `origin_domain`, `transfer_status`, `delta_vs_archive` (vs the 29-file Step-2 archive at `wiki/survey/README.md`).

---

## 0. P0 gate — the recognized open problems (named by 2024-26 literature, with metrics)

| ID | Problem (who names it) | Metric | Domain |
|---|---|---|---|
| **P-TXT-1** | **Intrinsic self-correction degrades reasoning accuracy, and published self-correction gains were oracle-label artifacts** — Huang et al., ICLR 2024 (arXiv:2310.01798): "improvements vanish when oracle labels are not available." | Accuracy delta after correction rounds: GPT-4 GSM8K 95.5→91.5→89.0; GPT-3.5 CommonSenseQA 75.8→**38.1** | text-LLM |
| **P-VLM-1** | **Self-generated critiques are unhelpful or detrimental, and VLM critique fails specifically at *visual perception*** — VISCO, CVPR 2025 (arXiv:2412.02172), 24 LVLMs; corroborated by SCL, ACL Findings 2025 (arXiv:2410.04055): VLMs cannot self-correct at inference without external feedback. | Post-correction accuracy / critique F1 on VISCO; human-critique vs self-critique gap | VLM |
| **P-SP-1** | **Prompt-only LLM correction of ASR over-corrects and hallucinates — in the low-error regime it *increases* error rates** — Gu et al. 2024/2026 (arXiv:2405.15216: "latency and hallucination concerns," LLMs struggle where precise correction is needed); RLLM-CF 2025 (arXiv:2505.24347) names the hallucination problem and builds a 3-stage verification pipeline against it. | WER/CER delta vs ASR baseline | speech |
| **P-SP-2** | **The n-best oracle gap (o_nb / o_cp) is real headroom, but closing it beyond o_nb currently requires *training* the corrector** — HyPoradise, NeurIPS 2023 D&B (arXiv:2309.15701) defines the oracles and shows only LoRA-tuned GER "surpass[es] the upper bound of traditional re-ranking." Training-free closure by the speech model itself is the unoccupied cell (yardstick memo §5, row (a)). | WER vs o_nb (re-ranking ceiling) and o_cp (compositional ceiling) | speech |

All method claims below anchor to these four.

---

## 1. WHY — the problem each line exists to answer

- **Text-LLM (Self-Refine, Reflexion, critique line).** WHY: single-pass generation leaves quality on the table; can the *same frozen model* recover it by critiquing and rewriting its own output? Self-Refine (arXiv:2303.17651) answers for open-ended quality; Reflexion (arXiv:2303.11366) answers for sequential decision/code tasks *where an external verifiable signal exists*; Huang et al. exist because the first two were being over-read — they re-ask the question with oracle access removed and inference budget matched (anchor P-TXT-1).
- **VLM.** WHY: VLM reasoning errors are dominated by *perception* errors (mis-seeing), so the text recipe was imported to fix them. VISCO exists to measure whether the critic can even detect perception errors (it largely cannot — anchor P-VLM-1); SCL exists because inference-time self-correction failed, asking whether the *attempt traces* are still useful as training data.
- **Speech (GER/HyPoradise-class).** WHY: 30 years of n-best rescoring is capped by o_nb — the answer may not be in the list (anchor P-SP-2). GER reframes correction as *generation*: map the n-best list to a transcription, possibly containing tokens no hypothesis had. Ma et al. (arXiv:2307.04172) ask the training-free version (can frozen ChatGPT do it?); ProGRes (arXiv:2409.00217) asks the hybrid version (prompt-generate new hypotheses, then rescore); RobustGER (arXiv:2401.10446) extends to noise robustness. Crucially: **this column is not self-correction** — a *different, text-only* LLM corrects the ASR model's output. The speech model never critiques itself.

## 2. HOW — mechanical differences

| Axis | Text-LLM Self-Refine | Text-LLM Reflexion | Text-LLM critique line | VLM (VISCO / SCL) | Speech GER-class |
|---|---|---|---|---|---|
| Loop target | own free-text output | own *policy/attempt*, across trials | same loops, controls added | own multimodal reasoning chain | **another model's** n-best output |
| Feedback source | self-generated NL critique | **external verifiable reward** (unit tests, env success) verbalized into memory | oracle removed; budget matched | self-critique (fails) vs human critique (works) vs forced re-grounding (LookBack) | ASR confidence scores, n-best agreement; verifier stage (RLLM-CF); never the audio itself in the frozen setting |
| What changes per iteration | the draft | the *plan* + episodic memory buffer | — | the reasoning chain, optionally after re-attending the image | hypothesis text (select, edit, or generate new) |
| Fence | training-free | training-free (no weight updates) | training-free (diagnosis) | VISCO/LookBack training-free; **SCL gradient-trained (DPO)** | Ma/ProGRes/TAP training-free; **HyPoradise H2T-LoRA & RobustGER gradient-trained (LoRA)**; Gu et al. trained specialized model |
| Grounding in raw input | n/a (text is the input) | n/a | n/a | **the differentiator**: critic must re-perceive the image | **absent** — the frozen corrector sees text only; audio grounding exists only in trained multimodal variants |

The mechanical spine across all three: **generate → critique/score → regenerate-or-select**. The columns differ in (i) *who* critiques (self vs external verifier vs separate text LLM), (ii) whether the critic can *re-access the raw modality*, and (iii) whether the loop's lift is realized at inference (training-free) or distilled into weights (SCL, GER-LoRA).

## 3. WHAT — measured outcomes (ladder-tagged)

| Claim | Effect | fence | ladder | origin_domain → transfer_status | anchor | delta_vs_archive |
|---|---|---|---|---|---|---|
| Self-Refine: ~20% abs. avg improvement, 7 tasks, GPT-3.5/ChatGPT/GPT-4; gains concentrated in open-ended preference tasks, smallest on math | +20% abs (avg) | training-free | **(b) unsplit**; post-Huang, the surviving reasoning share is closer to **b1** (style/format movement) | llm → vlm: attempted & failed at inference (SCL); speech: **untransferred** (no omni self-refine) | P-TXT-1 | **new** |
| Reflexion: HumanEval pass@1 91% vs GPT-4 80%, no weight updates, unit-test feedback | +11pp | training-free | **(c) realized** — ρ high *only because reward is verifiable*; matches memo §6 "(c) may be EASIEST" where reward = task success | llm → speech: **partial** (ASR-confidence-guided loops, ProGRes scoring) | P-TXT-1 (as the oracle-labeled regime Huang fences off) | **new** |
| Huang et al.: intrinsic self-correction *lowers* accuracy (GPT-4 GSM8K 95.5→89.0 after 2 rounds; GPT-3.5 CSQA 75.8→38.1); prior gains = oracle stopping | negative | training-free | **(c) negative**: self-critique as label-free selector has ρ ≤ 0 on reasoning | llm → vlm: **replicated** (VISCO, SCL); speech: **replicated as over-correction** (P-SP-1) | P-TXT-1 | **new** |
| Huang et al. **[MATCHED-BUDGET]**: at 9 responses, GSM8K GPT-3.5 — multi-agent debate 83.0 vs self-consistency **88.2**; debate "significantly underperforms simple self-consistency" at equal call count | −5.2pp vs SC | training-free | (c): plurality vote > self-critique per unit budget — text-domain replication of memo §6 row (c) | llm; speech transfer untested at matched budget | P-TXT-1 | **new** (self-consistency itself archived) |
| VISCO: model critiques "less helpful and sometimes detrimental"; human critiques lift correction; 3 failure modes (can't critique perception; reluctance to say no; exaggerated error-propagation); LookBack (re-attend image before critique) +up to 13.5% critique/correction | +13.5% (LookBack) | training-free | critique gap = **(c) negative**; LookBack = partial **(b2)** recovery via forced re-grounding | vlm → speech: **untransferred** ("re-listen before critique" has no omni analog yet) | P-VLM-1 | **new** |
| SCL: VLMs fail iterative inference self-correction; DPO on self-generated correction preferences improves *direct* generation | positive post-training | **gradient-trained** (out-of-fence; positioning) | background — field routed around inference-time failure into weights | vlm | P-VLM-1 | **new** |
| HyPoradise: 334K+ hyp-transcription pairs; **H2T-LoRA (LLaMA-13B + LoRA) surpasses o_nb**, the re-ranking upper bound; prompted LLMs "can even correct tokens missing in the N-best list" | beats o_nb (trained); ICL weaker | **gradient-trained** headline; ICL arm training-free | **(a)-failure remedy**: support injection beyond frozen q₀'s list; o_nb/o_cp = the (a) measurement instrument | speech-native (corrector = text llm) | P-SP-2 | **new** (memo-anticipated: §6 "GER/Hyporadise oracle tables") |
| RobustGER: language-space noise embedding + LLM finetuning; up to **53.9%** WER correction improvement on noisy sets | −53.9% rel (best) | **gradient-trained** (out-of-fence; headroom positioning) | (a)-remedy magnitude under noise | speech-native | P-SP-2 | **new** |
| Ma et al. 2307.04172: frozen ChatGPT, zero/1-shot; **N-best-constrained** selection/correction yields gains on transducer + AED ASR across test sets; unconstrained generation is the risky arm | gains (constrained) | **training-free** | constrained = **(c)**-like selection; unconstrained = (a)-expansion with P-SP-1 risk | speech-native | P-SP-1, P-SP-2 | **archived** (in Step-2 bibliography; sibling arXiv:2409.09554 also archived) |
| ProGRes: zero-shot prompted *generation* of new hypotheses + rescoring (ASR confidence + LLM sequence score); **5-25% rel WER** improvement (Llama-3-Instruct / GPT-3.5 / GPT-4-Turbo), SLT 2024 | −5-25% rel | **training-free** | **(a) support expansion**, realized label-free via confidence-fused rescoring (partial (c)) | speech-native (text-LLM-over-ASR caveat: **the omni does not expand its own support**) | P-SP-2 | new to archive bibliography; referenced in yardstick memo §5 |
| Gu et al. 2405.15216: compact trained corrector 1.5/3.3 WER (LS clean/other), 15× fewer params, beats LLM correction in low-error regime | LLM-negative framing | trained (positioning) | names the **(b2)-failure** of prompt-only correction | speech-native | P-SP-1 | **new** |

**Negative findings (first-class):** (i) intrinsic self-correction on reasoning is net-negative without external feedback — replicated in **all three domains** (Huang; VISCO/SCL; P-SP-1 over-correction); (ii) no paper found in which a frozen **speech/omni model corrects its own output from re-listening to the audio** — the entire speech column delegates correction to a text LLM that never hears the signal (searched this session across GER/HyPoradise/ProGRes/RLLM-CF lineage; consistent with the memo's "omni expands its own support" unoccupied cell); (iii) HyPoradise's oracle-beating result does not exist in the training-free arm — frozen-LLM ICL stays below the fine-tuned line.

**House numbers (stage-1 directional only):** ASR H_fix +0.0418 @ N=8/SNR-5 confirms (a)-mass exists in-house; MBR null + memory-selector exact zero give house prior ρ≈0 for ASR — *consistent with* the three-domain (c)-negative pattern above, not independent proof.

**Closure fence flag:** Reflexion's episodic memory buffer accumulates verbal reflections across trials. Any transfer proposal that extends this to a **cross-session accumulating store collides with the closed NO-GO question** (2026-07-03 decision §10, r1-r3) — within-episode reflection is fine; persistent accumulation requires an owner amendment.

---

## TRANSFER VERDICT

**Import first (ranked):**
1. **The Huang control discipline, before any mechanism.** Any W1/W4 correction-loop or re-prompting experiment must pre-register (i) no oracle stopping and (ii) a **matched-budget self-consistency/plurality baseline** — in the only controlled text-domain test, self-consistency beat the fancier loop by 5.2pp at equal call count. This is a controls import, and it is free.
2. **Reflexion's regime restriction:** run iterative loops **only where a verifiable reward exists** (W1's WER/exact-match rewards qualify). The one large positive self-correction number in any domain (80→91 pass@1) is entirely conditional on external verifiable feedback; intrinsic critique is net-negative in all three columns.
3. **LookBack as the one mechanically-new transferable idea:** force the frozen omni model to **re-attend the audio and verify each claim of its own transcript before critiquing** ("re-listen before you rewrite"). It is the only VLM-column mechanism with a positive training-free delta (+13.5%) against the perception-critique failure mode, it is untransferred to speech (verified-empty), and it directly operationalizes the house **b2 acoustic-grounding certification** — distinguishing genuine audio-grounded correction from text-prior hallucination.

**Biggest known risk (from the VLM failure modes):** **the critic is modality-blind.** VISCO's first failure mode — the model critiques logic but cannot critique *perception*, compounded by "reluctance to say no" — predicts that an omni model asked to self-correct ASR will keep its acoustic errors and fluently rewrite the text around them, i.e., exactly the over-correction/hallucination that P-SP-1 already documents as *WER-increasing* in the low-error regime. Mitigation is import #3 plus a do-no-harm gate (accept a correction only when an external verifiable score does not worsen), never unconstrained self-refinement.

---

## Sources (all resolved 2026-07-04)

1. Self-Refine: Iterative Refinement with Self-Feedback — Madaan et al., 2023-03-30 — https://arxiv.org/abs/2303.17651 — [new]
2. Reflexion: Language Agents with Verbal Reinforcement Learning — Shinn et al., 2023-03-20 (v4 2023-10-10) — https://arxiv.org/abs/2303.11366 — [new]
3. Large Language Models Cannot Self-Correct Reasoning Yet — Huang et al., ICLR 2024, 2023-10-03 — https://arxiv.org/abs/2310.01798 — [new]
4. VISCO: Benchmarking Fine-Grained Critique and Correction… — Wu et al., CVPR 2025, 2024-12-03 — https://arxiv.org/abs/2412.02172 — [new]
5. Self-Correction is More than Refinement (SCL) — ACL Findings 2025, 2024-10-05 — https://arxiv.org/abs/2410.04055 / https://aclanthology.org/2025.findings-acl.331/ — [new]
6. HyPoradise — Chen et al., NeurIPS 2023 D&B, 2023-09-27 — https://arxiv.org/abs/2309.15701 (proceedings PDF verified) — [new, memo-anticipated]
7. RobustGER — Hu et al., ICLR 2024 spotlight, 2024-01-19 — https://arxiv.org/abs/2401.10446 — [new]
8. Can Generative LLMs Perform ASR Error Correction? — Ma et al., 2023-07-09 — https://arxiv.org/abs/2307.04172 — [**archived**; sibling arXiv:2409.09554 and TAP arXiv:2309.15649 also archived]
9. ProGRes: Prompted Generative Rescoring on ASR n-Best — SLT 2024, 2024-08-30 — https://arxiv.org/abs/2409.00217 — [new to bibliography; memo §5-referenced]
10. Revisiting ASR Error Correction with Specialized Models — Gu et al. (Apple), 2024-05-24 (rev 2026-03-16) — https://arxiv.org/abs/2405.15216 — [new] · supporting anchor: RLLM-CF — https://arxiv.org/abs/2505.24347 — [new]


---

# 3W: prompt search/optimization (APE-OPRO vs VLM vs speech-TAP)

All sources verified. Composing the 3W deliverable now.

---

# 3W Scan — Prompt Search/Optimization: text-LLM (APE/OPRO/GEPA) × VLM prompt optimization × speech instruction prompting

**Mode:** deep-research `three-way-scan` (WHY/HOW/WHAT) · **Date:** 2026-07-04 · **Verification:** all links fetched and resolved 2026-07-04 · **Archive baseline:** `wiki/survey/README.md` (29 files, 93+ sources) — every source below carries `delta_vs_archive`.

## P0 — Recognized open problems this triple answers (named by 2024–26 literature)

- **PA-1 Prompt-format instability (text).** Semantically equivalent prompt formats move few-shot accuracy by **up to 76 points** on LLaMA-2-13B; single-format evaluation is methodologically unsound — named by Sclar et al., ICLR 2024 (FormatSpread). *Ladder: this spread is (b1) format-reachability evidence — format alone moves the metric.*
- **PA-2 Manual-prompt bottleneck under gradient inaccessibility.** Task performance "depends significantly on prompt quality" while gradients are unavailable for proprietary/frozen models — named by OPRO (ICLR 2024) for text and by Liu et al. (CVPR 2024) for closed-weight VLMs.
- **PA-3 RL-adaptation rollout cost.** GRPO-class RLVR needs thousands of rollouts per task adaptation; scalar rewards waste the information in language traces — named by GEPA (2025, rev. Feb 2026).
- **PA-4 Audio-LLM instruction unreliability.** "Different instructions of the same intention can yield drastically different outcomes" on large audio-LLMs — named by AHAMask (2025); AudioBench (2024) runs a prompt-template robustness analysis on audio-LLMs (its body-level finding that SALMONN is least robust across templates surfaced via search excerpt; not independently re-verified from the abstract — caution tag). Archive corroboration: Dynamic-SUPERB Phase-2 task gaps; ALICE format-vs-accuracy split (`delta_vs_archive: in-archive`).

---

## Column 1 — Text-LLM prompt search (origin_domain: llm)

**WHY:** PA-1 + PA-2 + PA-3 — hand prompts are brittle and expensive; the instruction is the only optimizable free variable on a frozen model.

**APE — Large Language Models Are Human-Level Prompt Engineers** · 2022 (ICLR 2023) · https://arxiv.org/abs/2211.01910 · `delta_vs_archive: new (named as class in yardstick memo §4, never archived as citation)`
- HOW: LLM proposes instruction candidates from input–output demos; candidates scored by target-model performance and selected. **Fence: training-free** (no weights touched; selection uses a labeled scoring set).
- WHAT: human-level or better instructions on **19/24** NLP tasks. *Ladder: (b) reachability — quantifies that instruction choice alone reaches mass a default prompt does not; b2-leaning (accuracy metrics), with labeled selection, so it does NOT establish (c).*

**OPRO — Large Language Models as Optimizers** · ICLR 2024 · https://arxiv.org/abs/2309.03409 · `delta_vs_archive: new`
- HOW: meta-prompt carries the trajectory of (prompt, score) pairs; optimizer-LLM proposes the next candidate; iterate. **Fence: training-free**; scores computed on labeled training examples.
- WHAT: **up to +8% GSM8K, up to +50% BBH** over human prompts. *Ladder: (b2) — the single largest published quantification of H_prompt − H_fix anywhere; exactly the quantity the yardstick memo §2 calls "zero-measured" for omni speech. problem_anchor: PA-1/PA-2.*

**GEPA — Reflective Prompt Evolution Can Outperform Reinforcement Learning** · 2025, rev. 2026-02 · https://arxiv.org/abs/2507.19457 · `delta_vs_archive: archive-named (GEPA Pareto rule cited in agent-memory-skills design), first verified citation here`
- HOW: sample rollouts → natural-language reflection on failures → mutate prompts → keep the **Pareto frontier** of candidates (non-regression rule). **Fence: training-free** (weights frozen; the gradient-trained GRPO arm is the *comparison*, not the method).
- WHAT: beats GRPO by **~6% avg, up to 20%, with up to 35× fewer rollouts** (per rev. Feb-2026 abstract); beats MIPROv2 by >10%. **MATCHED-BUDGET FLAG:** this is the rare rollout-budget-accounted training-free-vs-gradient comparison — the strongest WHAT in the whole triple. *Ladder: (b2). problem_anchor: PA-3.*

**Counter-evidence — Are LLMs Good Prompt Optimizers?** (Ma et al., 2024) · https://arxiv.org/abs/2402.02101 · `delta_vs_archive: new`
- WHAT: optimizer-LLMs "struggle to identify the true causes of errors… biased by their own prior knowledge"; gains partly from "unpredictable behaviors of the target models." *Ladder: background/anti — reflection faithfulness is not guaranteed; part of measured H_prompt may be noise exploitation.*

**FormatSpread** (Sclar et al., ICLR 2024) · https://arxiv.org/abs/2310.11324 · `delta_vs_archive: new` — the PA-1 anchor; also a *method*: report performance ranges over sampled formats, no weight access. **Fence: training-free.** *Ladder: (b1).*

---

## Column 2 — VLM prompt optimization (origin_domain: vlm)

**WHY:** CLIP-class zero-shot accuracy hinges on hand templates ("a photo of a {}"); closed weights block white-box tuning (PA-2, VLM form).

**CuPL — customized prompts via LLM** · ICCV 2023 · https://arxiv.org/abs/2209.03320 · `delta_vs_archive: new`
- HOW: text-LLM generates class-descriptive sentences; CLIP ensembles them. **Fence: training-free.**
- WHAT: **>1 point ImageNet zero-shot** gain, no training. *Ladder: (b) — b1/b2-unsplit pending the WaffleCLIP control below.*

**LLM as Black-Box Optimizer for VLMs** (Liu et al., CVPR 2024) · https://arxiv.org/abs/2309.05950 · `delta_vs_archive: new`
- HOW: chat-LLM hill-climbs natural-language CLIP prompts from textual feedback on scored candidates; no gradients, no logits. **Fence: training-free.**
- WHAT: 1-shot, 11 datasets: **+1.5% avg over white-box (gradient-trained) CoOp**; prompts transfer across VLM backbones. *Ladder: (b2) with labeled 1-shot scoring; transfer_status of the OPRO recipe into VLM: **native**.*

**Evolutionary prompt optimization on VLMs** (Bharthulwar et al., ICLR 2025 Workshop) · https://arxiv.org/abs/2503.23503 · `delta_vs_archive: new`
- HOW: evolutionary search over system prompts on frozen VLMs. **Fence: training-free.**
- WHAT: ~**50% relative** on select MathVista/M3CoT tasks; emergent tool-invocation strategies. *Ladder: (b2), workshop-grade.*

**Failure-mode pair (the risk column):**
- **CoCoOp** (CVPR 2022) · https://arxiv.org/abs/2203.05557 · `delta_vs_archive: new` — documents that **CoOp** (**fence: gradient-trained** soft prompts, out-of-fence positioning evidence) overfits base classes: "learned context is not generalizable to wider unseen classes." Optimized prompts can *lose* to hand prompts off-distribution. *Ladder: background (generalization risk of prompt search).*
- **WaffleCLIP** (ICCV 2023) · https://arxiv.org/abs/2306.07282 · `delta_vs_archive: new` — **random character/word descriptors match LLM-generated semantic descriptors** across many classification tasks; gains largely ensemble averaging, not semantics. *Ladder: the canonical b1-vs-b2 misattribution result — a within-VLM replication of the ALICE lesson.*

---

## Column 3 — Speech instruction prompting (origin_domain: speech)

**WHY:** PA-4 — audio-LLM behavior swings with same-intent instructions, and the field's response so far is *manual* prompting or *trained* bypasses, not search.

**TAP — Task-Activating Prompting** (Yang et al., ASRU 2023) · https://arxiv.org/abs/2309.15649 · `delta_vs_archive: in-archive (icl-fewshot lane)`
- HOW: hand-designed causal instruction+demonstration dialogue sequence "activates" a frozen text-LLM for post-ASR rescoring/correction over N-best lists. **Fence: training-free** (the below-oracle result combines fine-tuning — that arm is **gradient-trained**, out-of-fence).
- WHAT: frozen-LLM ICL rescoring **competitive with domain-tuned LMs** on ATIS/WSJ. *Ladder: (b) on the speech pipeline — but the prompt is fixed and hand-made: it proves a good prompt exists (support), not that search finds it. Transfer caveat (memo §6): text-LLM-over-ASR, not an audio-LLM hearing audio.*

**Evolutionary Prompt Design for LLM-Based Post-ASR Correction** (Sachdev, Wang & Yang, SLT 2024 GenSEC) · https://arxiv.org/abs/2407.16370 · `delta_vs_archive: new — nearest existing transfer of Column-1 machinery into speech`
- HOW: EvoPrompt-style evolutionary refinement of prompts for N-best correction on CHiME-4. **Fence: training-free.**
- WHAT: improved GenSEC challenge scores (abstract carries no headline WER; body not re-verified). *Ladder: (b), weakly quantified. **transfer_status: partial** — the optimizer wraps a text-LLM over ASR hypotheses; the audio front-end is outside the search loop.*

**AHAMask** (Guo et al., 2025) · https://arxiv.org/abs/2509.01787 · `delta_vs_archive: new`
- HOW: replaces instructions entirely — trains a binary attention-head mask (trainable params = head count) on the frozen audio-LLM backbone. **Fence: trained-head-on-frozen.**
- WHAT: comparable or **better than instruction prompting** on single and composite tasks. *Ladder: background/positioning — evidence that instruction-reachable task mass exists inside the frozen model ("functional pathways"), reached here by labels+gradients instead of prompt search. It bounds what (b) search should aim for.*

**Archive cross-refs** (`in-archive`, not re-fetched): Dynamic-SUPERB / Phase-2 (instruction-benchmark gaps), ALICE (format vs accuracy), MiMo-Audio (few-shot emergence) — the speech column's problem documentation.

---

## Cross-column synthesis

- **Common WHY:** on a frozen model the instruction is a free, high-variance input variable; all three columns exist because hand-set instructions leave measurable performance on the table (PA-1/2/4) and gradient adaptation is costly or impossible (PA-2/3).
- **Divergent HOW:** text-LLM = *closed-loop scored search* over instructions (propose→score→iterate: APE→OPRO→GEPA, increasingly reflection- and Pareto-driven); VLM = the same recipe ported natively (LLM-BBO, evolutionary VLM) *plus* generate-and-ensemble (CuPL); speech = **no closed loop on the audio-LLM at all** — hand-crafted activation sequences (TAP), search only on the text-LLM post-processor (2407.16370), or abandoning instructions for trained masks (AHAMask).
- **Strongest WHAT:** GEPA's matched-budget result (≥GRPO, up to 35× fewer rollouts) — training-free prompt evolution beating gradient RL under budget accounting; runner-up OPRO's +8/+50-point quantification of prompt-space headroom.
- **Unresolved global gap (verified-empty, 3 searches, 2026-07-04):** no published APE/OPRO/GEPA-class *automatic instruction search executed against an audio/omni-LLM consuming raw audio*, with WER/accuracy reported. Queries: (i) "automatic prompt optimization audio language model … APE OPRO"; (ii) audio-LLM prompt-sensitivity benchmarks (find sensitivity, no search); (iii) "prompt/instruction optimization + speech LLM + evolutionary/WER" (nearest hit is the text-LLM post-ASR paper). This is precisely the **H_prompt − H_fix "zero published quantification for omni speech models"** cell of the yardstick memo §2 — a first-class negative result, and the campaign's center of gravity confirmed still open.

## TRANSFER VERDICT

**Import first:** a **GEPA/OPRO-class scored instruction-search loop run directly on the frozen audio-LLM** (Qwen-Audio/Omni class), scoring K instruction candidates × N rollouts with the house verifiable speech rewards (WER/EM) on a small labeled dev slice — labels used *offline at search time only*, model training-free throughout. This is the cheapest direct measurement of **H_prompt(T,K,N) − H_fix(T,N)** — condition (b) — and GEPA's Pareto non-regression rule is already endorsed in the archive's design synthesis. In-house directional prior (OUR repo, **stage-1 directional only**): MInDS-14 +0.126 retrieval-surface lift, b1/b2-unsplit; ASR H_fix anchor +0.0418 @N=8/SNR-5. Note the fence nuance: this measures (b), not (c) — offline labeled prompt selection is legitimate and distinct from the unsolved per-utterance label-free selector (ρ≈0 house prior). Closure-fence check: a per-task offline search run is inside the fence; a *continuously accumulating cross-session prompt-evolver* would collide with the 2026-07-04 NO-GO — do not build that variant.

**Biggest known risk (from the VLM column's failure modes):** **WaffleCLIP-style misattribution** — measured prompt gains may be ensembling/format regularization (b1), not semantic task activation (b2); on speech this compounds with ALICE's format-vs-accuracy finding. Mandatory controls for any speech import: (1) random/shuffled-instruction "waffle" baseline at equal K; (2) label-sensitivity + acoustic-grounding checks (b1/b2 split per memo §3); (3) held-out-task generalization to catch CoOp-style dev-slice overfitting of the winning prompt; (4) Ma-et-al. caution — do not trust optimizer-LLM reflections as explanations, trust only the scored deltas.

## Sources (all fetched and resolved 2026-07-04)

1. APE, Zhou et al., ICLR 2023 — https://arxiv.org/abs/2211.01910 — `new`
2. OPRO, Yang et al., ICLR 2024 — https://arxiv.org/abs/2309.03409 — `new`
3. GEPA, Agrawal et al., 2025 (rev. 2026-02) — https://arxiv.org/abs/2507.19457 — `archive-named, first verified citation`
4. Ma et al., "Are LLMs Good Prompt Optimizers?", 2024 — https://arxiv.org/abs/2402.02101 — `new`
5. FormatSpread, Sclar et al., ICLR 2024 — https://arxiv.org/abs/2310.11324 — `new`
6. Liu et al., LLM as Black-Box Optimizer for VLMs, CVPR 2024 — https://arxiv.org/abs/2309.05950 — `new`
7. WaffleCLIP, Roth et al., ICCV 2023 — https://arxiv.org/abs/2306.07282 — `new`
8. CuPL, Pratt et al., ICCV 2023 — https://arxiv.org/abs/2209.03320 — `new`
9. CoCoOp, Zhou et al., CVPR 2022 — https://arxiv.org/abs/2203.05557 — `new`
10. TAP, Yang et al., ASRU 2023 — https://arxiv.org/abs/2309.15649 — `in-archive`
11. Sachdev et al., Evolutionary Prompt Design for Post-ASR Correction, SLT 2024 — https://arxiv.org/abs/2407.16370 — `new`
12. AHAMask, Guo et al., 2025 — https://arxiv.org/abs/2509.01787 — `new`

Auxiliary (verified): Bharthulwar et al., ICLR 2025 W — https://arxiv.org/abs/2503.23503 (`new`); AudioBench, Wang et al., 2024 — https://arxiv.org/abs/2406.16020 (`new`; SALMONN-least-robust detail is body-level, caution-tagged). Archive cross-refs not re-fetched: Dynamic-SUPERB (2309.09510), Phase-2 (2411.05361), ALICE (2603.20433), MiMo-Audio (2512.23808).


---

# 3W: best-of-N + verifier selection (text vs VLM vs speech)

All sources verified. Composing the 3W deliverable now.

# 3W Comparison — Best-of-N + Verifier/Reward Selection: text-LLM vs VLM vs speech

**Mode:** ars-3w (three-way-scan) · **Date:** 2026-07-04 · **Yardstick:** conditions (a)/(b1)/(b2)/(c) per `wiki/2026-07-04-sufficiency-yardstick-memo.md` · **Archive baseline:** step-2 survey index (29 files) — `delta_vs_archive` tagged per claim. All URLs resolved 2026-07-04.

---

## P0 — Recognized open problems (named by 2024–26 literature, with metric and namer)

| # | Problem (task-level deficiency) | Metric | Who names it | Column |
|---|---|---|---|---|
| P1 | **The verification gap**: repeated-sampling coverage scales log-linearly over 4 orders of magnitude, but label-free selection (majority vote, reward models) plateaus beyond ~100 samples — MATH/Llama-3-8B-Instruct coverage 79.8%→95.3% (100→10k samples) while RM-selection moves only 38.7%→39.8%. "Building robust verifiers remains an open problem." | solve-rate vs coverage upper bound | Brown et al. 2024, "Large Language Monkeys," [arXiv:2407.21787](https://arxiv.org/abs/2407.21787) (2024-07-31) | text |
| P2 | **Inference-time reward hacking / RM over-optimization**: BoN win-rate is non-monotone in N under an imperfect proxy reward (optimum N*) | proxy-vs-gold reward divergence at growing N | Gao et al. 2022 [arXiv:2210.10760](https://arxiv.org/abs/2210.10760); HedgeTune [arXiv:2506.19248](https://arxiv.org/abs/2506.19248) — both **in-archive** | text |
| P3 | **Multimodal verifiers are perception-blind**: generative VLM reward models "predominantly fail at basic visual perception tasks rather than reasoning"; GPT-4o scores only 65.4% on 1,250 preference pairs; inference-time-scaling benefit varies sharply with judge capacity | pairwise judgment accuracy | VL-RewardBench, Li et al. 2024, [arXiv:2411.17451](https://arxiv.org/abs/2411.17451) (2024-11-26) | vlm |
| P4 | **The ASR N-best oracle gap is not closable by the recognizer's internal scores**: eleven CTC-internal selection strategies yield no significant WER gain over greedy; the oracle mass is real but unreachable acoustically | WER vs N-best oracle WER | Novosad 2026, "Anatomy of the CTC Oracle Gap," [arXiv:2606.23306](https://arxiv.org/abs/2606.23306) (2026-06-22) — **memo-cited, URL now verified** | speech |
| P5 | **ρ (selection-realizability) for frozen *omni* speech models is unmeasured**: zero published quantification of label-free selector gain over sampled pools from an omni model; our C1 is the only in-house anchor | selector gain / oracle headroom | verified-empty search, 2026-07-03 delta scan + yardstick memo §2 — **negative finding, first-class** | speech |

Every method claim below anchors to one of P1–P5.

---

## Column A — text-LLM: verifier-guided test-time scaling / reward-model BoN

### Scaling LLM Test-Time Compute Optimally… (Snell et al.)
Source: arXiv | Year: 2024 | Link: https://arxiv.org/abs/2408.03314 · `delta_vs_archive: new` · `origin_domain: llm` · `fence: trained-head-on-frozen` (PRM verifier + frozen policy) · `problem_anchor: P1/P2` · `transfer_status: untransferred` (no speech instance found)

- **WHY:** fixed inference budget — how to spend it (sample-and-select vs sequential revision) instead of scaling parameters.
- **HOW:** PRM-guided search (best-of-N weighted, beam, lookahead) + adaptive revision; **compute-optimal allocation conditioned on prompt difficulty**.
- **WHAT:** >4× efficiency over naive best-of-N at **matched budget** (⚑ matched-budget evidence); easy prompts favor revision, hard prompts favor search. Ladder: (c) — realization via *trained* verifier, positioning evidence for our fence.

### Large Language Monkeys (Brown et al.)
Source: arXiv | Year: 2024 | Link: https://arxiv.org/abs/2407.21787 · `delta_vs_archive: new` · `origin_domain: llm` · `fence: training-free` (sampling + automatic or learned verifiers) · `problem_anchor: P1` · `transfer_status: partial` (pass@k exists in speech only as oracle-WER tables)

- **WHY:** is candidate *support* or candidate *selection* the bottleneck of repeated sampling?
- **HOW:** scale N to 10k; separate coverage (pass@k, oracle) from realized accuracy under majority vote / RM selection.
- **WHAT:** coverage 79.8→95.3% while RM-selection 38.7→39.8% at the *same* 10k samples (⚑ matched-budget). Ladder: coverage = (a) SUPPORT positive; selection plateau = (c) negative at scale. This is the text-domain twin of our C1 oracle-vs-MBR split.

### Scalable Best-of-N Selection via Self-Certainty (Kang, Zhao & Song)
Source: arXiv | Year: 2025 | Link: https://arxiv.org/abs/2502.18581 · `delta_vs_archive: in-archive` (D3 selector delta, verified) · `origin_domain: llm` · `fence: training-free` · `problem_anchor: P1` · `transfer_status: untransferred to speech`

- **WHY:** reward-model BoN is compute-heavy; self-consistency needs discrete answers — open-ended tasks lack a label-free selector.
- **HOW:** score each candidate by the policy's own output-distribution confidence (KL from uniform), aggregate across samples; no external model.
- **WHAT:** scales with N where majority voting saturates; combines with SC on reasoning. Ladder: (c) positive, text-native. **This is the highest-priority untransferred cell for speech.**

In-archive background (fence `training-free`, ladder (c)): self-consistency [arXiv:2203.11171](https://arxiv.org/abs/2203.11171); BoN KL theory [arXiv:2401.01879](https://arxiv.org/abs/2401.01879); soft-BoN [arXiv:2505.03156](https://arxiv.org/abs/2505.03156).

---

## Column B — VLM test-time scaling

### VisualPRM (Wang et al., InternVL)
Source: arXiv | Year: 2025 | Link: https://arxiv.org/abs/2503.10291 · `delta_vs_archive: new` · `origin_domain: vlm` (mechanism imported from llm PRMs) · `fence: trained-head-on-frozen` (8B PRM selects for frozen policies) · `problem_anchor: P1→P3` · `transfer_status: untransferred` (no audio PRM found)

- **WHY:** multimodal reasoning BoN lacks a step-level verifier; outcome RMs and self-consistency underperform.
- **HOW:** train an 8B multimodal PRM on 400K auto-generated step labels (MC-rollout correctness); select best-of-8 by min/avg step score.
- **WHAT:** +5.9 points avg across seven reasoning benchmarks even for InternVL2.5-78B; beats ORM and self-consistency at the *same* pool (⚑ matched-budget selector comparison). Ladder: (c) realized — but only by paying gradient training on the verifier side.

### VL-RewardBench (Li et al.)
Source: arXiv | Year: 2024 | Link: https://arxiv.org/abs/2411.17451 · `delta_vs_archive: new` · `origin_domain: vlm` · `fence: positioning (benchmark)` · `problem_anchor: P3` · `transfer_status: untransferred` (no speech reward-model benchmark exists — verified-empty in archive scans)

- **WHY:** VL generative reward models are deployed as BoN judges without a hard test.
- **HOW:** 1,250 human-verified preference pairs spanning hallucination detection, perception, reasoning; correlate judge accuracy with downstream BoN gain.
- **WHAT:** GPT-4o 65.4%; small judges near chance; **failures concentrate in basic perception, not reasoning**; judge accuracy correlates with BoN gain (up to +9.8 pts on MMMU-Pro when the judge is strong). Ladder: (c) boundary-condition — the verifier itself is the failure point. **This is the failure mode the speech column must import as a warning.**

### VisVM (Wang et al.)
Source: arXiv | Year: 2024 | Link: https://arxiv.org/abs/2412.03704 · `delta_vs_archive: new` · `origin_domain: vlm` · `fence: trained-head-on-frozen` (TD-trained value net guides a frozen VLM's stepwise search) · `problem_anchor: P3` · `transfer_status: untransferred`

- **WHY:** sentence-level CLIP-style rewards are myopic; hallucinations appear downstream of locally-plausible steps.
- **HOW:** TD-learned value model anticipates future sentence quality; guides stepwise decoding search instead of post-hoc BoN.
- **WHAT:** fewer hallucinations + richer detail vs greedy and vs CLIP-scored search; self-training on selected captions lifts downstream benchmarks. Ladder: (c) via trained value head; the *hallucination-amplification* motivation is the transferable lesson.

---

## Column C — speech best-of-N / MBR

### Re-evaluating MBR Decoding for ASR (Jinnai)
Source: arXiv | Year: 2025 (rev. 2026-05) | Link: https://arxiv.org/abs/2510.19471 · `delta_vs_archive: in-archive` · `origin_domain: speech` (mechanism from MT) · `fence: training-free` · `problem_anchor: P4/P5`

- **WHY:** MBR is standard in MT; does consensus selection over samples beat beam search for ASR/ST at all?
- **HOW:** sample pools from Whisper (En/Ja), select by pairwise utility (overlap-based), compare to beam search.
- **WHAT:** MBR **outperforms beam search in most settings** — offline-accuracy regime. Ladder: (c) positive for encoder-decoder ASR. Tension with our C1 MBR null on a frozen *omni* chat model is itself a P5 datum: pool geometry from an instruct-prompted omni model may differ from Whisper's.

### Anatomy of the CTC Oracle Gap (Novosad)
Source: arXiv | Year: 2026 | Link: https://arxiv.org/abs/2606.23306 · `delta_vs_archive: in-archive (memo-cited); URL verified today` · `origin_domain: speech` · `fence: training-free` (frozen RoBERTa utility, no tuning) · `problem_anchor: P4`

- **WHY:** N-best oracle mass exists; can any *internal* score of the recognizer reach it?
- **HOW:** eleven CTC-internal selection strategies (all null — first-class negative) vs MBR with a **frozen LM pseudo-log-likelihood as the utility**.
- **WHAT:** LibriSpeech test-other 5.96%→5.42% WER (~9% rel, p<0.0001): the oracle gap is *linguistically* recoverable but *acoustically* exhausted. Ladder: (c) positive — the only external label-free-selector positive in speech, and it works by **swapping the utility function, not the pool**.

### HyPoradise (Chen et al.) + ProGRes (Pusateri et al.)
HyPoradise: https://arxiv.org/abs/2309.15701 (NeurIPS 2023) · `delta_vs_archive: new — fills the SC-16 gap the /ars-reviewer panel flagged` · `fence: gradient-trained` (fine-tuned corrector) — positioning only.
ProGRes: https://arxiv.org/abs/2409.00217 (SLT 2024) · `delta_vs_archive: memo-named, URL verified` · `fence: training-free` (prompted frozen text-LLMs over a separate ASR) · `origin_domain: llm-over-speech` · `problem_anchor: P4→(a)`

- **WHY:** if selection ceilings at the N-best oracle, generate *new* hypotheses instead of picking.
- **HOW:** HyPoradise — fine-tuned LLM maps N-best→transcript; ProGRes — zero-shot prompted GPT-4/Llama-3 hypotheses appended to the n-best, then rescored.
- **WHAT:** HyPoradise **surpasses the n-best oracle** (only with fine-tuning); ProGRes 5–25% rel WER with no gradients. Ladder: (a) SUPPORT-expansion — but both are text-LLM-over-ASR pipelines; "the omni expands its own support" remains the unoccupied cell (memo §5).

### Our C1 anchor — ⚠ stage-1 directional only
Artifact: `D:\chao_workspace\exploring-l4-intelligence\projects\speech-mllm-training-free-rl\_repro\asr_bon_llamacpp_snr5.json` · `fence: training-free` (frozen Qwen3-Omni-30B Q8_0, llama.cpp) · `problem_anchor: P5`

- **HOW:** 144 LibriSpeech-style utts + SNR-5 noise, temp 0.8, pool N=8, pooled over 3 generation seeds; oracle-WER vs overlap-utility MBR on identical pools (⚑ matched-budget by construction).
- **WHAT (directional):** greedy WER 0.1183; **oracle reduction +0.0418 [0.0289, 0.0564]** at N=8; **MBR-consensus +0.0037 [−0.0082, 0.0170], n.s. — null**. Ladder: oracle = (a) SUPPORT positive (H_fix anchor); MBR null = (c) negative. Support exists; realization is the bottleneck.

---

## Cross-column synthesis

- **Common WHY:** all three columns confront the same decomposition — sampled pools contain far more correct mass than any label-free selector realizes (P1 = P4 = our oracle-vs-MBR split). The gap *between* coverage and selection, not coverage itself, is the named open problem in every domain.
- **Divergent HOW:** text moved from external reward models → **policy-internal signals** (self-certainty, self-consistency) after RM plateau/hacking (P2); VLM doubled down on **trained verifier heads** (VisualPRM, VisVM) because internal signals are too weak against perception errors — and then discovered the verifier itself is perception-blind (P3); speech still mostly uses **overlap-based MBR utilities**, with exactly one published utility-swap to a frozen-LM score (2606.23306). Speech is one mechanism-generation behind both other columns.
- **Strongest WHAT:** Brown et al.'s matched-budget coverage-vs-selection curves (text); VisualPRM's +5.9 avg at matched pools (VLM, but gradient-paid); Novosad's 9% rel WER with a purely frozen utility (speech, in-fence).
- **Unresolved global gap:** no domain has a label-free selector that tracks coverage as N grows; for *omni* speech models specifically, ρ is unmeasured in the literature (P5, verified-empty) — our C1 null is currently the only datum.

## TRANSFER VERDICT

**Import first (in-fence, within-query, no closure-fence collision):** the **utility-function swap** — replace the lexical-overlap MBR utility with policy-internal or frozen-LM scores over the *same* C1 pools: (i) self-certainty (arXiv:2502.18581, text-native, untransferred to speech) and (ii) frozen-LM pseudo-log-likelihood MBR utility (arXiv:2606.23306, already positive in speech at 9% rel). Rationale: C1 shows the pool already carries +0.0418 oracle headroom at N=8, so condition (a) is not failing — (c) is; both imports attack (c) directly, cost zero gradients, and are runnable on the existing artifact's stored pools (the per-utt pools are already in the JSON). ProGRes-style prompted self-generation of new hypotheses is the second-priority import, but it targets (a), which the anchor says is not yet the binding constraint. Neither import reduces to cross-session accumulating memory — no collision with the 2026-07-03 NO-GO closure.

**Biggest known risk (from the VLM column's failure modes):** **perception-blind verifiers** (VL-RewardBench P3). Every recommended selector scores *text* — linguistic plausibility, not acoustic fidelity. A frozen-LM utility will systematically prefer fluent-but-unfaithful transcriptions (the audio analogue of VLM judges missing basic visual facts, and of VisVM's hallucination-amplification motivation), which is precisely the b1/b2 artifact the yardstick memo splits: gains must be certified by label-sensitivity + acoustic-grounding controls before counting as (c) realization, and N should be capped near N* per the inference-time reward-hacking result (arXiv:2506.19248, in-archive) since a text-only proxy utility is exactly the imperfect reward that over-optimizes at large N.

**Sources (all resolved 2026-07-04):** [arXiv:2407.21787](https://arxiv.org/abs/2407.21787) · [arXiv:2408.03314](https://arxiv.org/abs/2408.03314) · [arXiv:2502.18581](https://arxiv.org/abs/2502.18581) · [arXiv:2503.10291](https://arxiv.org/abs/2503.10291) · [arXiv:2411.17451](https://arxiv.org/abs/2411.17451) · [arXiv:2412.03704](https://arxiv.org/abs/2412.03704) · [arXiv:2510.19471](https://arxiv.org/abs/2510.19471) · [arXiv:2606.23306](https://arxiv.org/abs/2606.23306) · [arXiv:2309.15701](https://arxiv.org/abs/2309.15701) · [arXiv:2409.00217](https://arxiv.org/abs/2409.00217) · in-house artifact `_repro/asr_bon_llamacpp_snr5.json` (stage-1 directional).


---

# 3W: agentic scaffolding, single-session (text vs GUI/VLM vs speech)

# 3W Comparison — Single-Session Agentic Scaffolding: Text Agents vs GUI/VLM Agents vs Speech-Agentic Pipelines

> ars-3w deliverable · Stage-1 survey · 2026-07-04 · scope = **single-session** scaffolds only (cross-episode/accumulating methods are fence-flagged per the NO-GO closure, see §6)

---

## 0. P0 gate — recognized open problems (named by 2024–26 literature, with metric)

| ID | Open problem | Who names it | Metric | Domain |
|---|---|---|---|---|
| **OP-1** | Voice agents complete roughly **half the tasks of matched text agents**: best full-duplex voice systems reach 31–51% pass@1 clean / 26–38% realistic vs **85% for a GPT-5 text agent** on the same τ²-bench domains — "30–45% of text capability retained" | τ-Voice (Ray, Dhandhania, Barres, Narasimhan, Mar 2026, [arXiv:2603.13686](https://arxiv.org/abs/2603.13686)) | pass@1 task success, τ²-bench domains under audio pipeline | speech |
| **OP-2** | Agent evaluations are not cost-controlled; complex scaffolds (Reflexion, LDB, LATS) are **Pareto-dominated by simple retry baselines at ~50× lower cost** on HumanEval — scaffold "gains" often measure spend, not method | Kapoor et al., "AI Agents That Matter", NeurIPS 2024 ([arXiv:2407.01502](https://arxiv.org/abs/2407.01502)) | accuracy-vs-dollar Pareto frontier | llm |
| **OP-3** | OS-level GUI agents achieve **12.24% vs 72.36% human** success; the named deficiency is **GUI grounding and operational knowledge**, not planning | OSWorld, NeurIPS 2024 ([arXiv:2404.07972](https://arxiv.org/abs/2404.07972)) | task success on 369 real desktop tasks | vlm |
| **OP-4** | Dual-control communication is a bottleneck distinct from reasoning: GPT-4.1 falls from 74%/56% (single-control airline/retail) to **34% in dual-control telecom**; a no-user ablation isolates ~11% pure communication/coordination cost | τ²-bench (Sierra, 2025, [arXiv:2506.07982](https://arxiv.org/abs/2506.07982)) | pass@1, Dec-POMDP dual-control env | llm→speech bridge |

OP-1 is the speech column's task-level deficiency; OP-2 is the methodological problem this whole 3W answers ("where do scaffolds add over plain prompting *at matched budget*"); OP-3 is the VLM failure mode we import as risk; OP-4 is the text-side decomposition that τ-Voice inherits.

---

## 1. WHY — the problem each line of work answers

**Text agents (ReAct / SWE-class).** WHY: single-shot prompting cannot (i) inject external evidence mid-generation or (ii) act on an environment with feedback. ReAct exists to fuse reasoning traces with tool actions against hallucination in knowledge tasks (problem_anchor: hallucination/error-propagation in chain-of-thought, named in [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)); SWE-agent exists because raw shell interfaces are unusable by LMs — the problem is **interface design**, not model capability (problem_anchor: prior best non-interactive RAG at 3.8% on SWE-bench, [arXiv:2405.15793](https://arxiv.org/abs/2405.15793)). A counter-literature exists *within the same column*: Agentless ([arXiv:2407.01489](https://arxiv.org/abs/2407.01489)) and Kapoor et al. (OP-2) exist because agentic autonomy itself was never validated against structured-but-non-agentic pipelines at matched cost.

**GUI/VLM agents.** WHY: the OP-3 human-agent gap. The column's diagnosis evolved from "planning is weak" to "**grounding is the binding constraint**": text-based observation (HTML/accessibility trees) is noisy and incomplete, and pixel-level grounding of intents to coordinates fails (UGround, ICLR 2025, [arXiv:2410.05243](https://arxiv.org/abs/2410.05243), problem_anchor: OP-3).

**Speech-agentic (tau2-voice class).** WHY: OP-1 + OP-4. Text agents pass τ-bench-style domains at 74–85%; putting the *same tasks* behind a full-duplex audio channel (accents, noise, telephony compression, interruptions, backchanneling) halves completion. τ-Voice's key attribution: **79–90% of failures stem from agent behavior**, not audio quality per se — i.e., the deficit is claimed to be largely scaffold/behavior-addressable rather than front-end-limited. This line of work exists to measure that gap; almost no work yet exists to *close* it training-free (verified-empty, §5).

---

## 2. HOW — mechanical differences

| Axis | Text (ReAct/SWE-class) | GUI/VLM | Speech-agentic (tau2-voice class) |
|---|---|---|---|
| Scaffold primitive | interleaved thought→action→observation loop (ReAct); or **fixed 3-phase pipeline** localize→repair→validate (Agentless); or ACI: curated commands + guarded feedback (SWE-agent) | planner–grounder split (SeeAct-V): frozen VLM plans in text, separate grounding module maps intent→pixel coordinates | cascaded ASR→LLM(tools)→TTS, or end-to-end speech-to-speech API + tool-calling; full-duplex adds streaming turn-taking control |
| What the scaffold conditions on | tool returns (retrieved text, interpreter output, test results) | screenshots; grounding output | user audio + tool returns, under real-time pressure (barge-in, latency) |
| Verifiability of reward | high (tests pass, answer EM) → selection over retries is realizable | medium (env-state checkers in OSWorld/WebArena) | **high** (τ²-style DB-state checks) — the yardstick's condition (c) is *easiest* here |
| Where it breaks | scaffold cost inflation (OP-2); intrinsic self-correction degrades accuracy without external feedback ([arXiv:2310.01798](https://arxiv.org/abs/2310.01798)); component interference — all-components scaffolds lose to 1–3-component subsets ([arXiv:2605.05716](https://arxiv.org/abs/2605.05716), single-author, supporting-grade) | grounding errors compound over long horizons; fix that worked (UGround) is a **gradient-trained module**, not a scaffold | turn-taking/interruption handling, instruction retention under disfluency (Full-Duplex-Bench-v3, [arXiv:2604.04847](https://arxiv.org/pdf/2604.04847), archived); communication overhead (OP-4) |
| Fence tag | training-free (frozen LM + prompt/interface); LATS = training-free tree search | scaffold composition training-free, but UGround grounder = **gradient-trained** component | evaluated systems training-free at inference; the *improving* methods are weight-updating (CORTIS, SoulX-Duplug — archived A4-09) |

---

## 3. WHAT — measured outcomes (matched-budget evidence flagged ★)

| Claim | Number | Budget-matched? | origin_domain / transfer_status | Ladder | delta_vs_archive |
|---|---|---|---|---|---|
| ReAct beats imitation/RL baselines on ALFWorld/WebShop | +34% / +10% absolute with 1–2 shots ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629)) | ✗ (vs trained baselines, not matched-sample plain prompting) | llm / **partial** (voice tool-use benchmarked, ReAct-style ablation absent in speech) | (a)-failure routing: external support injection | new |
| ★ Simple retry baselines Pareto-dominate Reflexion/LDB/LATS on HumanEval | ~50× lower cost at equal-or-better accuracy ([arXiv:2407.01502](https://arxiv.org/abs/2407.01502)) | ★ **yes — the defining cost-controlled result** | llm / **untransferred** to speech | (a)+(c): repeated sampling + verifiable-reward selection | new |
| ★ Agentless (fixed pipeline, no autonomy) beats open-source agents on SWE-bench Lite | 32.00% at $0.70/issue, highest performance *and* low cost ([arXiv:2407.01489](https://arxiv.org/abs/2407.01489)) | ★ yes (cost reported and dominated) | llm / untransferred | (b) reachability via structured conditioning | new |
| SWE-agent ACI vs shell-only: interface design alone moves resolve rate | 12.5% vs prior 3.8%; shell-only ablation markedly worse ([arXiv:2405.15793](https://arxiv.org/abs/2405.15793)) | partial (same model, same task; iteration budget looser) | llm / untransferred | (b2) genuine-accuracy reachability via interface | new |
| ★ Intrinsic self-correction *degrades* reasoning accuracy | performance drops after self-correction without external feedback ([arXiv:2310.01798](https://arxiv.org/abs/2310.01798), ICLR 2024) | ★ yes-negative (extra calls, worse result) | llm / untransferred | **(b2) negative**: re-prompting alone doesn't move accuracy | new |
| OSWorld: best VLM agent vs human | 12.24% vs 72.36%, deficiency = GUI grounding + operational knowledge ([arXiv:2404.07972](https://arxiv.org/abs/2404.07972)) | n/a (benchmark) | vlm / background | background (perception bottleneck) | new |
| UGround/SeeAct-V: vision-only grounding beats accessibility-tree scaffolds | outperforms text-observation baselines across web/desktop/mobile ([arXiv:2410.05243](https://arxiv.org/abs/2410.05243)) | ✗ (adds a trained model) | vlm / background — **fix is out-of-fence (gradient-trained)** | background | new |
| τ²-bench: dual-control cost | GPT-4.1 74/56% → 34% telecom; no-user ablation ≈ 11% communication cost ([arXiv:2506.07982](https://arxiv.org/abs/2506.07982)) | yes-internally (same model, ablated env) | llm / **native to speech setting** (τ-Voice extends it) | (b) decomposition: communication vs reasoning load | new (τ-bench 2406.12045 archived) |
| τ-Voice: voice vs text agents | 31–51% clean / 26–38% realistic vs 85% text; 79–90% failures = agent behavior; telecom clean: xAI 58% vs 20–28% others ([arXiv:2603.13686](https://arxiv.org/abs/2603.13686)) | ✗ — modality gap, **not** scaffold-vs-plain at matched budget | speech / **native** | (b) reachability headroom claim, b1/b2-unsplit; (a) unmeasured in speech-agentic (confirms yardstick §6) | **new — key delta**; complements archived tau2-voice README (A4-05) |
| Component stacking can interfere destructively | single-tool agent beats all-components by 32% F1 on HotpotQA ([arXiv:2605.05716](https://arxiv.org/abs/2605.05716)) | partial (no cost control) | llm / untransferred | (b) caution: scaffold ≠ monotone conditioning | new, supporting-grade |

---

## 4. Cross-column synthesis

1. **Where scaffolds provably add at matched budget (text column):** (i) *interface/structure* — SWE-agent's ACI and Agentless's fixed decomposition move a verifiable end-metric on the same frozen model (b2 evidence); (ii) *external evidence injection* — ReAct-class tool grounding (support injection, the yardstick's (a)-failure family). **Where they provably don't:** autonomy per se (Agentless), intrinsic self-reflection (Huang et al.), and component maximalism (CCI) — at matched budget these lose to plain prompting + retries + a verifier.
2. **The VLM column's lesson is a boundary condition:** when the binding constraint is *perception-side* (GUI grounding), no amount of training-free scaffolding closed OP-3; the working fix was a gradient-trained grounding module. Scaffolds only pay when the model's latent competence is reachable-but-unconditioned.
3. **The speech column has the measurement but not the method:** τ-Voice/τ²/FDB-v3 give verifiable-reward environments (condition (c) is *easiest* here, per yardstick §6), and τ-Voice's failure attribution (79–90% agent behavior) implies large (b)-type headroom — but that attribution is the paper's own, unreplicated, and b1/b2-unsplit.

## 5. Negative findings (first-class)

- **Verified-empty:** no speech-agentic study isolating scaffold contribution vs plain prompting at matched compute/cost was found (targeted searches over τ-Voice, tau2-bench voice README, FDB-v3, and generic "voice agent scaffold ablation / cost-controlled" queries, 2026-07-04). The Kapoor-style cost-controlled Pareto analysis has **zero speech instantiation**. This is the unoccupied cell.
- No cascaded-vs-end-to-end scaffold comparison with controlled budget surfaced inside τ-Voice's abstract/HTML (fetch partially blocked; body-level check pending — flagged, not claimed).

## 6. Closure-fence flags

Reflexion, ExpeL, AWM, JitRL (archived A3-headroom lane) are **cross-episode accumulating** methods — they collide with the closed NO-GO question (2026-07-03 decision §10, r1–r3) if imported as "memory across sessions." They are cited here only as the *contrast class*; everything recommended below is strictly within-session. LATS (archived CV-lane) is within-episode tree search — in scope, but note it is one of the scaffolds Pareto-dominated in OP-2.

---

## 7. TRANSFER VERDICT

**Import first (ranked):**
1. **The cost-controlled scaffold-ablation protocol (OP-2, origin llm → untransferred).** Before building any speech scaffold: run plain-prompt + best-of-N-retry with the τ²-style verifiable reward as the mandatory baseline, and report accuracy-vs-cost Pareto. This is simultaneously (i) the field's verified-empty cell, (ii) directly executable on house best-of-N machinery (W1; our ASR +0.0418 anchor is stage-1 directional only), and (iii) the cleanest instantiation of condition (c) — speech-agentic is the one family where reward = verifiable task success, so selection-realizability may escape the house ρ≈0 prior observed on ASR.
2. **The Agentless/ACI lesson (origin llm → untransferred): structure over autonomy.** Fixed dialogue decomposition (intake → verify-identity → resolve → read-back-confirm) plus a speech-ACI (guarded tool feedback, explicit confirmation subroutines for OP-4's communication overhead) is the cheapest (b)-lever, and is exactly what τ-Voice's 79–90% agent-behavior failure attribution predicts should pay. Do **not** import self-reflection loops — they are matched-budget-negative in the origin domain.

**Biggest known risk (from the VLM column's failure mode):** the **binding-constraint trap**. GUI scaffolding stagnated at 12% because the bottleneck was perception-side grounding, and the fix that worked (UGround) was gradient-trained — out-of-fence. The speech analogue: if τ-Voice's degradation is actually dominated by acoustic perception / full-duplex turn-taking rather than agent behavior, training-free scaffolds hit the same wall, and the literature's known fixes (SoulX-Duplug's trained state predictor, CORTIS fine-tuning — archived A4-09/A4-10) are weight-updating. τ-Voice's own attribution argues otherwise but is unreplicated — so the *first measurement* of any transfer effort must be re-deriving that failure split (audio-front-end vs agent-behavior) under matched budget, because it decides whether the training-free fence contains the problem at all.

**Sources (all resolved 2026-07-04):** [ReAct, arXiv:2210.03629](https://arxiv.org/abs/2210.03629) · [SWE-agent, arXiv:2405.15793](https://arxiv.org/abs/2405.15793) · [AI Agents That Matter, arXiv:2407.01502](https://arxiv.org/abs/2407.01502) · [Agentless, arXiv:2407.01489](https://arxiv.org/abs/2407.01489) · [LLMs Cannot Self-Correct Reasoning Yet, arXiv:2310.01798](https://arxiv.org/abs/2310.01798) · [OSWorld, arXiv:2404.07972](https://arxiv.org/abs/2404.07972) · [UGround, arXiv:2410.05243](https://arxiv.org/abs/2410.05243) · [τ²-bench, arXiv:2506.07982](https://arxiv.org/abs/2506.07982) · [τ-Voice, arXiv:2603.13686](https://arxiv.org/abs/2603.13686) · [Cross-Component Interference, arXiv:2605.05716](https://arxiv.org/abs/2605.05716) — plus archived: tau-bench 2406.12045, tau2-voice README, FDB-v3 2604.04847, LATS 2310.04406 (wiki/survey, A4/A3/CV lanes).


> **D5b correction (SC-10):** where this lane cited retry/self-refine cost as "~50× lower", the source [103] supports up to ~50× only for LATS; Reflexion/LDB are ≈1.5×, with no significant accuracy advantage for simple retry. Carried into the survey §3.12 revision.
