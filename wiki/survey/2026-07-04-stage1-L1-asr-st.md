# Stage-1 lane L1 — ASR + Speech Translation

> Stage-1 problem-definition campaign lane · 2026-07-04 · workflow `wf_d7b939e9-c37` · methodology:
> CLAUDE.md three-stage section (Stage 1: survey-grounded argumentation; in-house numbers
> directional-only). Yardstick: [[2026-07-04-sufficiency-yardstick-memo]]. Every claim carries
> origin-domain (llm/vlm/speech), transfer-status, fence, ladder-condition and problem-anchor
> tags; every URL adversarially verified; P0 gate enforced (anchor-less claims struck).

## Open problems (P0-compliant: task-level, metric-named, literature-anchored)

### P1-longtail-entity — ladder: mixed

Web-scale frozen ASR (Whisper-class) and audio-LLMs still fail disproportionately on rare words and named entities: Whisper 'faces difficulty in recognising rare words like domain-specific terms' despite 680K h of training audio, and ContextASR-Bench formalizes the deficiency for LALMs with entity-focused metrics. The strongest published fixes are gradient-trained (biasing-instruction fine-tuning: +45.6% rare-word recognition). Fence note: the sub-family of solutions that accumulate a personalized bias lexicon ACROSS sessions collides with the closed NO-GO (r1-r3) and needs owner amendment; per-session context injection does not.

**Metric:** entity-WER / B-WER / NE-WER and NE-FNR (ContextASR-Bench); rare-word recall

**Named by:** [ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark](https://arxiv.org/abs/2507.05727) (2025-07-08) · [Improving Rare-Word Recognition of Whisper in Zero-Shot Settings](https://arxiv.org/abs/2502.11572) (2025-02-17) · [RECOVER: Robust Entity Correction via agentic Orchestration of hypothesis Variants for Evidence-based Recovery](https://arxiv.org/abs/2603.16411) (2026-03-17)

### P2-noise-hallucination — ladder: mixed

Frozen ASR fabricates fluent content absent from the audio, concentrated on silence/disfluency/noise: ~1% of Whisper transcriptions contain entire hallucinated phrases, 38% of which carry explicit harms, with disparate rates for aphasia speakers (FAccT 2024). Label-free detection is unsolved training-free: text-metric heuristics reach only F1 23.6% and the best detectors are gradient-trained probes of decoder internals.

**Metric:** hallucination rate (% segments with fabricated phrases); harmful-content share; label-free detection F1; insertion-dominant WER under SNR sweeps

**Named by:** [Careless Whisper: Speech-to-Text Hallucination Harms (FAccT 2024)](https://arxiv.org/abs/2402.08021) (2024-02-12) · [From Text Metrics to Model Internals: A Study of Whisper ASR Hallucination Detection](https://arxiv.org/abs/2606.23060) (2026-06-22)

### P3-oracle-deployable — ladder: c

The n-best oracle-vs-deployable selection gap: large oracle WER headroom exists in sampled/beam pools, but label-free selectors realize only a small fraction. Model-internal confidence is exhausted (11 CTC-internal scoring strategies give no significant gain over greedy at G=16; score-WER correlation degrades with pool size), self-certainty stays significantly below oracle at every N in the text domain, and HyPoradise frames the reranking upper bound that only trained correction surpasses. House anchor (stage-1 directional only, W1 repo): oracle +0.0418 WER reduction @ N=8/+5 dB SNR vs MBR realizing ~0-10% of it.

**Metric:** rho = realized fraction of n-best oracle WER reduction by label-free selectors; WER gap to o_nb oracle

**Named by:** [The Anatomy of the CTC Oracle Gap: Acoustic Exhaustion and Linguistic Recovery](https://arxiv.org/abs/2606.23306) (2026-06-22) · [Scalable Best-of-N Selection for Large Language Models via Self-Certainty](https://arxiv.org/abs/2502.18581) (2025-02-25) · [HyPoradise: An Open Baseline for Generative Speech Recognition with Large Language Models (NeurIPS 2023 D&B)](https://arxiv.org/abs/2309.15701) (2023-09-27)

### P4-ger-limits — ladder: mixed

LLM-based generative error correction (GER/Hyporadise line) hits limits without external/acoustic grounding: zero-shot LLM correction can increase WER (unconstrained decoding introduces truncation/deletion errors) and needs N-best evidence plus constrained decoding to be safe; intrinsic self-correction without external feedback degrades performance in the origin (text) domain; and under acoustic noise GER quality collapses unless rescued by gradient-trained noise-aware tuning (RobustGER).

**Metric:** signed delta-WER pre-to-post LLM correction, especially OOD/noisy; entity recall after correction

**Named by:** [ASR Error Correction using Large Language Models](https://arxiv.org/abs/2409.09554) (2024-09-15) · [Large Language Models are Efficient Learners of Noise-Robust Speech Recognition (RobustGER, ICLR 2024)](https://arxiv.org/abs/2401.10446) (2024-01-19) · [Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024)](https://arxiv.org/abs/2310.01798) (2023-10-03)

### P5-lowres-st — ladder: mixed

Low-resource speech translation remains the family's weakest cell: a dedicated 2025 benchmark study concludes SpeechLLMs do NOT yet redefine SOTA against cascaded ASR+MT ('the latest LLMs may struggle with low-resource languages'), with cascaded 2-stage recipes still ahead for low-resource pairs; zero-resource ST is explicitly open (ICASSP 2025); and the strongest N-best-integration fix (GenTranslate) is LoRA fine-tuned, not training-free.

**Metric:** BLEU/COMET on CoVoST2 X->En low-resource pairs and FLEURS low-resource subsets, vs cascaded SOTA

**Named by:** [Reassessing Speech Translation for Low-Resource Languages: Do LLMs Redefine the State-of-the-Art Against Cascaded Models? (MRL @ EMNLP 2025)](https://aclanthology.org/2025.mrl-main.11/) (2025-11) · [Zero-resource Speech Translation and Recognition with LLMs (ICASSP 2025)](https://arxiv.org/abs/2412.18566) (2024-12-24) · [GenTranslate: Large Language Models are Generative Multilingual Speech and Machine Translators (ACL 2024)](https://arxiv.org/abs/2402.06894) (2024-02-10)

### P6-st-selection-blind — ladder: c

Label-free selection for speech translation is blocked at the reward: reference-free QE metrics for ST (including a SOTA SpeechLLM evaluator and the new SpeechCOMET) systematically ignore the audio signal and fail on speech-specific phenomena, and the standard deployable proxy (BLASER 2.0-QE) is a trained regression head. Consequently rho(ST) - the realized fraction of best-of-N oracle gain on ST candidates - is unmeasurable and unmeasured.

**Metric:** correlation of reference-free QE with human judgments on speech phenomena; realized fraction of BoN oracle COMET/BLEU gain over ST candidate pools

**Named by:** [Why We Need Speech to Evaluate Speech Translation](https://arxiv.org/abs/2605.28227) (2026-05-27) · [Seamless: Multilingual Expressive and Streaming Speech Translation (ships BLASER 2.0-QE)](https://arxiv.org/abs/2312.05187) (2023-12-08)


## Approach genealogy & evidence claims (cross-domain mandatory)

### C01-hyporadise-oracle — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: a · anchor: P3-oracle-deployable

HyPoradise (NeurIPS 2023 D&B) is the canonical quantification of ASR n-best headroom: 334K+ N-best/transcription pairs across domains, with oracle tables framing the reranking upper bound; its efficiently fine-tuned generative error correction achieves 'a breakthrough by surpassing the upper bound of traditional re-ranking based methods' by generating tokens missing from the N-best list. Establishes (a)-support magnitude for ASR, but the headline result is gradient-trained (the ICL variant is training-free and weaker).

**Sources:** [HyPoradise: An Open Baseline for Generative Speech Recognition with Large Language Models](https://arxiv.org/abs/2309.15701) (2023-09-27) · verified: True

*Origin-domain evidence:* NeurIPS 2023 D&B; 334K+ hypothesis-transcription pairs; abstract confirms 'surpassing the upper bound of traditional re-ranking based methods' and correcting tokens missing from the N-best list; verified by direct arXiv fetch 2026-07-04
*Speech-domain evidence:* native (speech-domain paper; mechanism imported from text-LLM prompting/finetuning)

### C02-progres-support-expansion — [duplicate] origin: **speech** · transfer: native · fence: training-free · ladder: a · anchor: P3-oracle-deployable

ProGRes (SLT 2024) shows a frozen instruction-tuned LLM can both GENERATE new candidate hypotheses beyond the ASR sampler's n-best (support expansion that moves the pool oracle itself) and rescore them, yielding 5-25% relative WER improvement, fully training-free. The lane's strongest in-fence (a)-failure remedy; 'the omni expands its own support' remains the unoccupied cell.

**Sources:** [ProGRes: Prompted Generative Rescoring on ASR n-Best](https://arxiv.org/abs/2409.00217) (2024-08-30) · verified: True

*Origin-domain evidence:* abstract confirms 'dynamically expand the n-best speech recognition hypotheses with new hypotheses generated through appropriately-prompted LLMs' and 5-25% relative WER improvement (Llama-3-Instruct/GPT-3.5/GPT-4 generators); re-verified by direct arXiv fetch 2026-07-04 (archived D3-5)
*Speech-domain evidence:* native (text-LLM-over-ASR pipeline)

### C03-tap-prompting — [duplicate] origin: **llm** · transfer: native · fence: training-free · ladder: b2 · anchor: P4-ger-limits

Task-activating prompting (TAP) ports the text-LLM prompting playbook to ASR error correction: a chained instruction/demonstration warm-up 'activates' a frozen LLM for N-best rescoring/GER without weight updates, achieving results competitive with rescoring by domain-tuned LMs on ATIS/WSJ. Genealogy anchor for instruct-prompt reachability (b2) on the correction surface.

**Sources:** [Generative Speech Recognition Error Correction with Large Language Models and Task-Activating Prompting (ASRU 2023)](https://arxiv.org/abs/2309.15649) (2023-09-27) · verified: True

*Origin-domain evidence:* prompt-chaining/task-activation is a text-LLM technique; abstract confirms 'rescoring only by in-context learning with frozen LLMs achieves results that are competitive with rescoring by domain-tuned LMs'; verified by direct arXiv fetch 2026-07-04
*Speech-domain evidence:* native (demonstrated on ASR N-best correction, ATIS/WSJ)

### C04-sicl-whisper — [new] origin: **llm** · transfer: native · fence: training-free · ladder: b2 · anchor: P1-longtail-entity

Speech-based in-context learning (SICL, ICASSP 2024): k labelled audio-text example pairs placed in frozen Whisper's context reduce WER by 32.3% average (36.4% with kNN example selection) on Chinese dialect isolated-word ASR, with considerable reductions for speaker adaptation and continuous speech - genuine accuracy movement (b2) from pure in-context conditioning, explicitly 'without gradient descent'.

**Sources:** [Can Whisper perform speech-based in-context learning? (ICASSP 2024)](https://arxiv.org/abs/2309.07081) (2023-09-13) · verified: True

*Origin-domain evidence:* ICL originates in text LLMs (GPT-3 class); SICL is its explicit port to a frozen speech model
*Speech-domain evidence:* native: 32.3%/36.4% relative WER reduction on frozen Whisper 'without gradient descent', all figures confirmed by direct arXiv fetch 2026-07-04

### C05-prompting-whisper — [new] origin: **llm** · transfer: native · fence: training-free · ladder: b2 · anchor: P5-lowres-st

PromptingWhisper (Interspeech 2023): pure prompt engineering on frozen Whisper (manipulating special tokens / concatenating another model's output) improves unseen-task performance 10-45% on AVSR, code-switched ASR, and speech translation on unseen pairs, sometimes beating supervised SOTA - direct speech-native evidence that prompt-space carries real task mass (b2) on a frozen speech model, including for ST.

**Sources:** [Prompting the Hidden Talent of Web-Scale Speech Models for Zero-Shot Task Generalization (Interspeech 2023)](https://arxiv.org/abs/2305.11095) (2023-05-18) · verified: True

*Origin-domain evidence:* prompt-engineering methodology from text LLMs
*Speech-domain evidence:* native: abstract confirms 'improve performance by 10% to 45% on the three zero-shot tasks, and even outperform SotA supervised models on some datasets' (AVSR, CS-ASR, ST on unseen pairs); verified by direct arXiv fetch 2026-07-04

### C06-opro-prompt-headroom — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P1-longtail-entity

OPRO (ICLR 2024) quantifies prompt-space headroom in the origin domain: LLM-driven discrete prompt search finds instructions beating human-written prompts by up to 8% (GSM8K) and up to 50% (Big-Bench Hard) - the class of measurement the yardstick memo identifies as the ONLY existing quantification of H_prompt. No application to WER/BLEU objectives on frozen speech/omni models exists (verified-empty search) - untransferred.

**Sources:** [Large Language Models as Optimizers (OPRO, ICLR 2024)](https://arxiv.org/abs/2309.03409) (2023-09-07) · verified: True

*Origin-domain evidence:* abstract confirms 'the best prompts optimized by OPRO outperform human-designed prompts by up to 8% on GSM8K, and by up to 50% on Big-Bench Hard tasks'; verified by direct arXiv fetch 2026-07-04
*Speech-domain evidence:* none found (2026-07-04 search: no OPRO/APE-class prompt search against WER on frozen Whisper/audio-LLMs)

### C07-gepa-prompt-evolution — [update] origin: **llm** · transfer: untransferred · fence: training-free · ladder: b2 · anchor: P4-ger-limits

GEPA (reflective Pareto prompt evolution) shows no-gradient prompt optimization can outperform weight-space RL: 'GEPA outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts' in the text domain - the strongest evidence that prompt-space headroom can rival gradient headroom. New use vs archive: as the b2 upper-reference for what K-instruction search could contribute to ASR correction prompts (archive A2-09 already proposes GEPA for speech skill text); still no published ASR/ST instance.

**Sources:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/abs/2507.19457) (2025-07-25) · verified: True

*Origin-domain evidence:* abstract quote confirmed by direct arXiv fetch 2026-07-04: 'GEPA outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts' (archived A2-09)
*Speech-domain evidence:* none found for ASR/ST objectives (2026-07-04 search)

### C08-multiprompt-mbr — [new] origin: **llm** · transfer: untransferred · fence: training-free · ladder: c · anchor: P3-oracle-deployable

Multi-prompt MBR (EMNLP 2024) is the exact text-domain operationalization of H_prompt minus H_fix plus a deployable selector: sampling candidates from a prompt bank yields 'a more diverse and higher quality candidate space than that of a single prompt', and MBR selection over that pool 'improves generation across tasks, models and metrics'. No speech instance found - the K-instructions x N-rollouts cell for ASR/ST is unoccupied.

**Sources:** [Improving Minimum Bayes Risk Decoding with Multi-Prompt (EMNLP 2024)](https://arxiv.org/abs/2407.15343) (2024-07-22) · verified: True

*Origin-domain evidence:* abstract quotes confirmed by direct arXiv fetch 2026-07-04: multi-prompt decoding from a prompt bank at inference-time; 'estimating a more diverse and higher quality candidate space than that of a single prompt'; 'multi-prompt improves generation across tasks, models and metrics'
*Speech-domain evidence:* none found (no multi-prompt candidate-pool study on ASR/ST; 2026-07-04 searches)

### C09-self-refine — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P4-ger-limits

Self-Refine (NeurIPS 2023): a single frozen LLM generating, critiquing, and revising its own output improves task performance ~20% absolute on average across 7 tasks with GPT-3.5/4, with no supervised training data, additional training, or RL - the text-LLM origin of iterative re-prompting. Speech transfer is partial: the GER line uses EXTERNAL n-best evidence rather than intrinsic self-refinement, and no self-refine loop on a frozen omni speech model was found.

**Sources:** [Self-Refine: Iterative Refinement with Self-Feedback (NeurIPS 2023)](https://arxiv.org/abs/2303.17651) (2023-03-30) · verified: True

*Origin-domain evidence:* abstract confirms 'improving by ~20% absolute on average in task performance' across 7 tasks (GPT-3.5/ChatGPT/GPT-4) and 'does not require any supervised training data, additional training, or reinforcement learning'; verified by direct arXiv fetch 2026-07-04
*Speech-domain evidence:* partial: GER/TAP refine ASR hypotheses but with external n-best evidence, not intrinsic self-feedback

### C10-self-correction-limits — [new] origin: **llm** · transfer: partial · fence: training-free · ladder: background · anchor: P4-ger-limits

The boundary condition on C09 from the origin domain: LLMs cannot intrinsically self-correct reasoning - without external feedback 'their performance even degrades after self-correction' (ICLR 2024). Predicts and explains the speech-side finding that unconstrained zero-shot LLM ASR correction can degrade output (truncation/deletion errors) unless grounded in n-best/lattice-constrained decoding (archived 2409.09554) - a background fence on how far prompted GER loops can go.

**Sources:** [Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024)](https://arxiv.org/abs/2310.01798) (2023-10-03) · verified: True

*Origin-domain evidence:* abstract quote confirmed by direct arXiv fetch 2026-07-04: 'LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction'
*Speech-domain evidence:* partial: 2409.09554 body (fetched 2026-07-04) documents unconstrained GPT-3.5 correction introducing truncation/deletion errors, fixed by N-best/lattice-constrained decoding - mirroring the text result

### C11-verifier-guided-bon — [new] origin: **llm** · transfer: partial · fence: trained-head-on-frozen · ladder: c · anchor: P3-oracle-deployable

The origin of verifier-guided best-of-N is Cobbe et al. 2021 (GSM8K): sample many candidate solutions and 'select the one ranked highest by the verifier'; 'verification scales more effectively with increased data than a finetuning baseline'. Speech transfer is partial and out-of-fence: ASR analogs (trained rescorers, NoRefER-class QE, decoder-state probes) are all gradient-trained; the training-free deployable verifier for ASR n-best is exactly the P3 gap.

**Sources:** [Training Verifiers to Solve Math Word Problems (GSM8K)](https://arxiv.org/abs/2110.14168) (2021-10-27) · verified: True

*Origin-domain evidence:* abstract quotes confirmed by direct arXiv fetch 2026-07-04: 'we generate many candidate solutions and select the one ranked highest by the verifier'; 'verification scales more effectively with increased data than a finetuning baseline'
*Speech-domain evidence:* partial: trained rerankers/QE exist for ASR (all gradient-trained, fence-tagged OUT); no training-free counterpart

### C12-mbr-mt-to-asr — [update] origin: **llm** · transfer: partial · fence: training-free · ladder: c · anchor: P6-st-selection-blind

MBR-with-neural-utility genealogy: Freitag et al. (TACL 2022) showed MBR decoding with BLEURT beats MAP/beam search in human evaluations for MT - 'model estimates and translation quality only vaguely correlate' - and the archived Re-evaluating-MBR paper (2510.19471) confirms the transfer to Whisper-class models, where MBR outperforms beam search in most evaluated settings on both ASR and ST. Update vs archive: adds the MT origin (2111.09388) and narrows the open cell - MBR/BoN with QE utilities (COMET/BLASER) over speech-LLM ST candidate pools, and the realized-vs-oracle fraction rho(ST), remain unquantified.

**Sources:** [High Quality Rather than High Model Probability: Minimum Bayes Risk Decoding with Neural Metrics (TACL 2022)](https://arxiv.org/abs/2111.09388) (2021-11-17) · [Re-evaluating Minimum Bayes Risk Decoding for Automatic Speech Recognition](https://arxiv.org/abs/2510.19471) (2025-10-22) · verified: True

*Origin-domain evidence:* Freitag abstract quotes confirmed by direct arXiv fetch 2026-07-04: 'model estimates and translation quality only vaguely correlate'; MBR+BLEURT 'results in significant improvement in human evaluations'
*Speech-domain evidence:* native for ASR and Whisper ST (2510.19471 fetched 2026-07-04: 'MBR decoding outperforms that of beam search in most of the experimental settings' on ASR and ST with Whisper-class models; archived ND11); missing: QE-utility selection over speech-LLM ST pools and any oracle-realization (rho) measurement

### C13-contrastive-decoding-vlm-to-audio — [new] origin: **vlm** · transfer: partial · fence: training-free · ladder: b2 · anchor: P2-noise-hallucination

Training-free contrastive decoding against hallucination originates in VLMs: VCD (CVPR 2024) contrasts output distributions from original vs distorted visual inputs to cut object hallucination with no training. The audio transfer exists but stops short of ASR: TCD (ACL 2026 Findings) contrasts next-token logits from original vs temporally-smoothed audio on frozen LALMs (consistent MMAU/AIR-Bench gains), and AVCD/AAD are its siblings - none targets ASR transcription hallucination under noise (Whisper-class), leaving the P2 training-free mitigation cell open.

**Sources:** [Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding (CVPR 2024)](https://arxiv.org/abs/2311.16922) (2023-11-28) · [Temporal Contrastive Decoding: A Training-Free Method for Large Audio-Language Models](https://arxiv.org/abs/2604.15383) (2026-04-16) · verified: True

*Origin-domain evidence:* VCD abstract confirmed by direct arXiv fetch 2026-07-04: 'a simple and training-free method that contrasts output distributions derived from original and distorted visual inputs'; 'significantly mitigates the object hallucination issue across different LVLM families'
*Speech-domain evidence:* partial: TCD (fetched 2026-07-04: smoothed slow-path vs original logit contrast; 'Experiments on MMAU and AIR-Bench show consistent improvements') and AVCD (2505.20862, training-free, AVHBench) apply contrastive decoding to LALM understanding benchmarks, not to ASR hallucination under noise

### C14-robustger-positioning — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: background · anchor: P2-noise-hallucination

RobustGER (ICLR 2024 spotlight, top 5%) is the gradient-trained ceiling for noise-robust correction: language-space noise embeddings extracted from the N-best list plus efficient LLM finetuning give up to 53.9% correction improvement in WER under noise - and it documents that 'directly incorporating noise embeddings from audio encoder could harm the LLM tuning due to cross-modality gap'. Positioning evidence: no training-free method currently recovers GER quality under noise.

**Sources:** [Large Language Models are Efficient Learners of Noise-Robust Speech Recognition (RobustGER, ICLR 2024)](https://arxiv.org/abs/2401.10446) (2024-01-19) · verified: True

*Origin-domain evidence:* abstract confirmed by direct arXiv fetch 2026-07-04: 'extract a language-space noise embedding from the N-best list'; 'up to 53.9% correction improvement in terms of word error rate'; cross-modality-gap caveat quoted verbatim
*Speech-domain evidence:* native (speech-domain paper)

### C15-contextasr-prompt-context — [new] origin: **speech** · transfer: native · fence: training-free · ladder: b2 · anchor: P1-longtail-entity

ContextASR-Bench shows prompt-injected context is a live training-free lever on the entity surface: frozen LALMs given coarse-grained (domain) or fine-grained (entity-list) context in the instruction are assessed on NE-WER/NE-FNR against the contextless setting, and 'LALMs outperform conventional ASR models by a large margin thanks to the strong world knowledge and context modeling of LLMs'. b2-leaning evidence (genuine entity accuracy movement), though label-sensitivity/acoustic-grounding controls in the yardstick's sense are absent, so b1/b2 not formally split.

**Sources:** [ContextASR-Bench: A Massive Contextual Speech Recognition Benchmark](https://arxiv.org/abs/2507.05727) (2025-07-08) · verified: True

*Origin-domain evidence:* verified 2026-07-04 by direct arXiv abstract fetch (40,000 entries, 300,000+ named entities, 10+ domains; LALMs-vs-ASR quote) plus HF dataset card confirming NE-WER/NE-FNR metrics and the three contextual evaluation settings (contextless / coarse-grained domain / fine-grained entity list)
*Speech-domain evidence:* native

### C16-gentranslate-nbest-st — [new] origin: **speech** · transfer: native · fence: gradient-trained · ladder: a · anchor: P5-lowres-st

GenTranslate (ACL 2024) proves the ST n-best pool contains enough information to beat top-1 decoding: an LLM fine-tuned on HypoTranslate (592K+ hypotheses-translation pairs, 11 languages) integrates N-best candidates into translations that significantly outperform SOTA direct-ST models on FLEURS/CoVoST-2/WMT. (a)-support evidence for ST, realized only out-of-fence; the training-free analog (prompted N-best integration for ST) was not found.

**Sources:** [GenTranslate: Large Language Models are Generative Multilingual Speech and Machine Translators (ACL 2024)](https://arxiv.org/abs/2402.06894) (2024-02-10) · verified: True

*Origin-domain evidence:* abstract confirmed by direct arXiv fetch 2026-07-04: HypoTranslate 'over 592K hypotheses-translation pairs in 11 languages'; 'significantly outperforms the state-of-the-art model' on FLEURS/CoVoST-2/WMT; ACL 2024, code open-sourced
*Speech-domain evidence:* native


## Training-free vs fine-tuned SOTA positioning

# L1 (ASR + ST) — training-free vs fine-tuned SOTA positioning

**Long-tail / entity ASR (P1).** Fine-tuned SOTA: biasing-instruction fine-tuning of Whisper (+45.6% rare-word, +60.8% unseen-word recognition, arXiv:2502.11572) and trie/neural deep-biasing lines. Training-free line: prompt-injected context on frozen LALMs (ContextASR-Bench NE-WER/NE-FNR contrasts across contextless/coarse/fine settings), SICL k-shot audio-text pairs (32.3–36.4% rel WER on dialects), kNN-Whisper datastore decoding (archived), RECOVER agentic entity correction (8–46% rel entity-WER, archived). The training-free biasing line is *thinning* (D3 negative re-affirmed): recent 2026 biasing work is predominantly gradient-trained.

**GER / correction (P4).** Fine-tuned SOTA: Hyporadise fine-tuned GER breaks the n-best reranking upper bound; RobustGER adds up to 53.9% correction improvement under noise. Training-free: TAP prompting (competitive with domain-tuned rescoring LMs) and ProGRes (5–25% rel WER) stay competitive but below tuned GER; the origin-domain boundary (intrinsic self-correction degrades without external feedback, ICLR 2024) explains why every safe training-free variant is n-best/evidence-grounded (constrained decoding, arXiv:2409.09554).

**Selection (P3).** Out-of-fence: trained verifiers (Cobbe line), NoRefER-class QE, decoder-state hallucination probes. In-fence: MBR (positive for Whisper ASR/ST, archived), frozen-LM MBR utility (9.0% rel, archived), self-certainty (below oracle at every N), internal confidence (statistically null at G=16) → ρ(ASR) small; house C1 numbers (oracle +0.0418 vs MBR ~0–10% realized) are stage-1 directional only.

**Speech translation (P5/P6).** Fine-tuned SOTA: GenTranslate (LLM fine-tuned over N-best, beats SOTA on FLEURS/CoVoST-2) and POTSA-class alignment; cascaded 2-stage recipes still beat SpeechLLMs on low-resource pairs (MRL @ EMNLP 2025). Training-free: PromptingWhisper's 10–45% zero-shot gains include unseen-pair ST — the main in-fence positive; multi-prompt MBR (EMNLP 2024) is the text-domain blueprint for K-prompt × N-sample ST pools but is untransferred, and ST selection is reward-blocked (QE metrics ignore audio; BLASER 2.0-QE is a trained head). Whisper-class ST MBR exists (arXiv:2510.19471) but no QE-utility selection over speech-LLM ST pools and no ρ(ST) measurement.

**Net for the house thesis.** In every sub-family the fine-tuned ceiling is documented and higher; the training-free lane's live levers are prompt-context injection, ICL demonstrations, prompted hypothesis generation/rescoring, contrastive decoding (audio transfer incomplete), and MBR — with the K-instruction prompt-space (H_prompt − H_fix) and the ST-selection reward being the two cells where literature offers no quantification at all.

## Negative findings (verified-empty searches & P0 strikes — first-class results)

- No published application of APE/OPRO/GEPA-class automatic prompt search to WER/BLEU objectives on a frozen speech or omni model (searched 2026-07-04: 'automatic prompt optimization OPRO APE speech recognition WER frozen Whisper audio LLM instruction search' and variants) — H_prompt(ASR/ST) has zero published quantification, confirming the yardstick memo's zero-measurement statement from the lane side.
- Multi-prompt candidate generation + MBR selection (Heineman et al., EMNLP 2024) has no speech instance: no study samples ASR/ST candidates across K instructions/prompts and selects label-free — the K-instructions x N-rollouts cell for ASR/ST is verified unoccupied (searches 2026-07-04).
- Contrastive-decoding hallucination mitigation transferred VLM->LALM (TCD arXiv:2604.15383, AVCD arXiv:2505.20862, AAD) but only onto audio-understanding benchmarks (MMAU/AIR-Bench/AVHBench); no instance targeting ASR transcription hallucination under noise on Whisper-class or omni models was found (searched 2026-07-04) — the P2 training-free mitigation cell is open.
- No oracle-vs-deployable best-of-N/MBR gap study on speech-translation outputs of speech-LLMs (COMET- or BLASER-selected BoN over ST candidate pools on CoVoST2/FLEURS) was found (searched 2026-07-04: 'minimum Bayes risk decoding speech translation COMET best-of-N candidate selection frozen model') — extends the archived D3 negative (S2S) to text-output ST. Scope caveat added by verifier: arXiv:2510.19471 does evaluate MBR on Whisper ST and finds it beats beam search, but with candidate-consensus utility and no oracle-realization measurement, so rho(ST) is unmeasured, not closed.
- Re-affirmed from archive (D3, 2026-07-03): no gradient-free reference-free WER predictor exists anywhere in the searched literature; training-free label-free ASR selection signals remain model-internal confidence (statistically null as a selector at G=16 per arXiv:2606.23306) and consensus/MBR — nothing new surfaced in this lane's 2026-07-04 searches to overturn it.
- Closure-fence note (not an empty search): the P1 solution sub-family 'accumulate a personalized bias lexicon across sessions' reduces to cross-session accumulating memory and collides with the closed NO-GO (decision doc section 10, r1-r3); it is flagged here and excluded from the problem's in-scope remedy set, while per-session context injection remains in scope.
- Verifier audit 2026-07-04 (this pass): all 29 unique source URLs across 6 problems and 16 claims resolved by direct fetch (arXiv abstracts; ACL Anthology landing page for the MRL 2025 paper; HF dataset card for ContextASR-Bench metrics); zero dead or mismatched links; 16/16 claims carry a problem_anchor matching a listed problem id, so no P0 strikes. Corrections applied: (i) C12 speech_evidence narrowed — arXiv:2510.19471 itself covers Whisper ST MBR (matches archived ND11 'ASR/ST'), so the open cell is QE-utility selection over speech-LLM ST pools + rho(ST); (ii) exact titles fixed (MRL 2025: 'Reassessing Speech Translation for Low-Resource Languages...' with URL switched from the unparseable PDF to the Anthology landing page; RECOVER full title); (iii) C03/C01 wording aligned to source text ('competitive with rescoring by domain-tuned LMs'; 'LoRA-tuned' softened to 'efficiently fine-tuned'). Paper-body figures not visible in abstracts — F1 23.6 (P2), self-certainty below oracle at every N (P3), SpeechCOMET (P6), BLASER 2.0-QE shipping in Seamless (P6) — were cross-confirmed against the archive's prior adversarial pass (D3-8, D3-1, D3-6, D3-7 respectively); P4's zero-shot-degradation clause was confirmed by a direct body fetch of arXiv:2409.09554 (unconstrained GPT-3.5 correction introduces truncation/deletion errors; constrained N-best/lattice decoding fixes it). Tag audit: all origin_domain/fence/ladder/transfer_status assignments consistent with the lane's conventions; note C12's fence 'training-free' follows the house convention that MBR with an off-the-shelf trained utility metric counts as training-free (no new training performed), mirroring the archived Re-evaluating-MBR tagging.