---
title: "Stage-1B round-2 local-fulltext method-path notes"
date: 2026-07-21
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
role: "WORKBENCH D2 path evidence; not canonical REC-2, occupancy, or novelty verdict"
---

# Stage-1B round-2 local-fulltext method-path notes

## Evidence boundary

All 26 priority-pass papers below passed the recorded abstract gate before this full-text pass. Their PDFs
were opened from the external survey store and all 26 now also have local e-prints. Four later
citation-triggered papers passed the same gate and were read; three have both renditions, while
`2503.12271` has a verified PDF and a retained bounded-retry e-print failure. PDF/e-print bytes are not Git
artifacts. The append-only full-text ledger retains arXiv URLs, timestamps, attempts, sizes, SHA-256 values,
and storage paths.

These are provisional D2 **method-path** notes with source locators. They deliberately distinguish a frozen
base model from all-components-weight-frozen execution, a pretrained readout from external new information,
and a deployable control signal from an oracle or diagnostic instrument. Canonical REC-2 transcription,
threat dual coding, H5 calibration, study-quality coding, and occupancy derivation remain separate work.

## Path cards

### Closest no-update control paths

| arXiv | System/control path | Boundary and adverse evidence | Full-text locator |
|---|---|---|---|
| 2511.11483 ImAgent | A single unified multimodal model receives observation history; a prompted policy controller chooses among naive generation/editing, CoT prompt enhancement, detail refinement, best-of-N, and `STOP`. The image and critique return to the same model, producing a real multi-call state/action loop without a separately trained controller. | No method-specific weight update or external evaluator is reported, but the path is image generation/editing rather than native speech. Reported gains conflate action composition with adaptive policy choice unless action-count/equal-budget controls are isolated. | §3.1–3.3 and Fig. 2 (pp. 4–7); Tables 1–2 and analysis (pp. 10–13). |
| 2512.19433 dMLLM-TTS | A diffusion MLLM generates multiple trajectories, uses its own image-understanding QA as Self-Verified Feedback, prunes and refines trajectories with Hierarchical Trajectory Search, and uses the same score for final selection. This is a same-core, multi-call, nonparametric search path. | Complexity falls from linear grid search `O(NT)` to `O(N+T)`, but the paper's own Table 2 shows GPT-4o/VILA judges can outperform intrinsic verification. The control path is close; verifier capability remains an attribution bottleneck. | §3.2–3.4 (pp. 3–5); Table 1 (p. 6); Table 2 (p. 8); §5. |
| 2602.04208 SCALE | The frozen VLA's token distribution yields self-uncertainty. Within one forward pass, uncertainty changes both action-sampling temperature and visual-attention temperature; low uncertainty sharpens/exploits, high uncertainty broadens/explores. | No added verifier or method training is required, but it needs white-box logits/attention and acts inside a task-trained VLA. It is a direct same-signal-to-look-and-act edge, not a black-box API path. | §3.2–3.3 and Fig. 2 (pp. 2–4); Table 1 (p. 6); Table 6 ablation. |
| 2510.05681 MG-Select | A frozen autoregressive VLA samples actions and compares its conditional token distribution with a condition-masked reference from the same VLA. Aggregated KL divergence becomes an endogenous confidence score for best-of-N action selection. | The base inference-only variant requires no new training or external verifier; an optional joint-training variant must be split as a different path. Both require token distributions and repeated action candidates. | Fig. 1 and §3 (pp. 2–4); Table 1 (p. 6); Table 5 ablations (p. 8). |
| 2604.15383 TCD | A unified audio-language model re-encodes the original waveform and a temporally blurred view, contrasts next-token logits, restricts the update to a candidate set, and activates it with an uncertainty/audio-reliance gate. | Training/label updates are absent and both views derive from the task-native waveform. The method requires decoder logits plus time-resolved audio states; §6 explicitly limits applicability to unified LALMs retaining such states. | §3 (pp. 3–5); Table 1 (p. 6); §6 (p. 9). |
| 2607.11801 IAAN | At inference, a native audio encoder is run on the real waveform and an unstructured-noise reference. Per-neuron activation contrast identifies acoustic neurons, which are amplified before decoding. | Strong native-audio and no-training/no-label evidence, but it is a white-box activation intervention rather than reward-guided sequential control. Improvements depend on the exact neurons and encoder locus, not merely intervention size. | §III (pp. 2–3); main comparisons/ablations (pp. 4–7); conclusion. |
| 2601.05159 VLI | A vision-language model detects conflict between visual evidence and linguistic confidence, localizes causal visual anchors, constructs anchor/context counterfactual states, and applies instance-specific latent steering. | No weight update is claimed, but hidden-state/attention access is required and the object is hallucination control in vision. Counterfactual construction adds compute and is itself a sensitivity point. | §3 (pp. 3–6); Table 1 (p. 6); limitations (p. 9). |
| 2604.11025 TTSP | The MLLM samples parallel perception traces containing reasoning plus zoom/crop tool calls, filters them by token-entropy reliability, stores confirmed/open-conflict knowledge, directs later rounds toward unresolved evidence, and finishes with reliability-weighted voting. | Crops are deterministic transforms of task-native pixels rather than outside answers. The loop is fixed by rounds/traces and needs multiple model/tool calls; it is a strong perception-search/memory path but not audio or omni-native. | Definition 1.1; Algorithm 1 and §3.2–3.6 (pp. 3–5); Tables 1–2. |
| 2504.11101 Consensus Entropy | Multiple VLM OCR outputs are compared in output space; inter-model agreement entropy verifies outputs, selects an ensemble answer, and routes difficult items to stronger models. | Training-free and same-cost controls are reported, but this is explicitly a multi-model ensemble topology rather than one frozen multimodal core. The signal is consensus, not self-verification from one model. | §3; Table 1 (p. 6); routing/ensemble results (pp. 7–9). |

### Frozen integration or decoding with an external component

| arXiv | System/control path | Why it does not automatically enter the strict intersection | Full-text locator |
|---|---|---|---|
| 2602.23306 ThinkOmni | An omni LLM consumes the multimodal input while an off-the-shelf textual LRM scores the same prefix. Their logits are contrastively fused, and a stepwise scaling term adapts guide strength from the two models' predictions. | No new training/data is used, but topology is two-model and requires shared vocabularies, logit access, and extra forward passes. The LRM cannot see the multimodal observation; modality specificity enters through the OLLM side of the contrast. | §3.1–3.3 (pp. 3–5); Tables 1–2 (pp. 6–7); Fig. 7; §6 limitation. |
| 2508.10016 LLM Orchestration | A text LLM emits closed-vocabulary tokens for expert selection, sequencing, and stop; a deterministic router enforces mappings/timeouts/fallbacks; evidence-keyed cross-modal memory persists finalized expert results; interruption cancels in-flight work. | Training-free applies to integration/control, not to the pretrained modality experts. It is a controller-plus-expert system, not a single omni-native core. The paper explicitly makes this narrower claim. | §1 contribution/boundary (pp. 2–3); §3 (pp. 5–7); Tables 1–3; §5 limitations. |
| 2508.11616 MRGD | Two separately built visual-grounding reward models score object precision and recall for partial generations. At each step, candidate continuations are sampled and reward-weighted before committing output tokens. | The MLLM may remain frozen, but learned external reward models are method components; strict all-components-frozen occupancy therefore fails. The work nevertheless supplies a direct reward-to-token-decision edge. | Algorithm 1 and §3 (pp. 3–4); Table 1 (p. 5); limitations (p. 9). |
| 2510.13804 OmniVerifier-TTS | A newly RL-trained OmniVerifier-7B critiques generated images, and a unified generator iteratively edits them using generative feedback; sequential TTS beats parallel best-of-N under the reported budget. | The verifier is explicitly trained on newly constructed verification data. It is a strong external-verifier comparator and measurement instrument, not a qualifying fully frozen path. The paper also documents broad weaknesses in untrained MLLM visual critics. | §3–4; Table 4 and sequential-TTS analysis; limitations/benchmark findings. |
| 2603.16253 EVPV | The policy self-reports step-wise visual premises; a trained constraint extractor predicts structured image facts once; checklist/constraint consistency gates an independent step verifier's rewards before best-of-N reranking. | Both constraint coverage and checklist completeness can fail. A global reliability value can spread a local misread across the whole trajectory, and self-reported dependency creates under-reporting/reward-hacking risk. External learned components exclude the path from strict occupancy. | §3.2–3.3 (pp. 4–6); Table 3 ablation (p. 9); limitations (p. 12); fidelity audits in appendices. |
| 2509.19831 SCORE | Text-to-audio candidates are guided by a standardized weighted combination of pretrained audio-quality and audio-text-alignment rewards, allowing an explicit quality/alignment trade-off. | Base generator weights are unchanged, but learned reward instruments and their calibration drive selection/guidance. Single rewards show opposing attribute trade-offs, so improvements cannot be credited to extra samples alone. | §2–3 (pp. 2–3); §4.1 and Table 1; §4.2 ablation. |
| 2606.08393 SMC-ITA | Video-to-audio generation is cast as sequential Monte Carlo search. Lookahead estimates multidimensional cross-modal reward, and systematic resampling reallocates trajectories over the generation path. | External reward instruments mediate the control signal. Matched-NFE results against best-of-N/beam help isolate search allocation, but native speech/understanding is not the object. | §II–III (pp. 2–3); main results/ablations (pp. 4–5). |
| 2604.12647 TRIAGE | A frozen audio-text encoder produces cheap label scores; uncertain respiratory examples escalate to structured descriptor matching and then retrieval-augmented LLM reasoning; a confidence threshold gives early exit. | No task-specific model training is used, but the high tier injects retrieved clinical text and uses a separate LLM. It is a useful information-boundary and budget-routing comparator, not a strict no-new-information single-core path. | Method overview (pp. 2–4); Table 1 and §5.1 (p. 7); routing analysis. |
| 2604.09155 CORA | A base GUI policy proposes an action; a separately trained Guardian estimates action-conditional risk; conformal calibration sets an execute/abstain threshold; rejected actions route to a Diagnostician. | Guardian training and calibration labels are method-specific components. Guarantees depend on exchangeability/weighted-shift assumptions and blockwise splitting. The path is important for stop/abstain safety, not strict training-free occupancy. | §3–4; Table 1 and §5.2 (p. 9); Appendix F assumptions. |

### Adverse, oracle, and diagnostic controls

| arXiv | Load-bearing result | Consequence for mapping | Full-text locator |
|---|---|---|---|
| 2512.11109 | Across open/closed VLMs and three benchmarks, best-of-N with external verification is most reliable for open models, while self-refinement can reduce accuracy; perceptual tasks show narrow or negative gains. | Never collapse “test-time scaling” into a universally positive treatment. Separate model capability, task type, selector, and candidate-supply effects. Methods differ across closed APIs because internal confidence is unavailable. | Tables 1–3 (§4); conclusion. |
| 2606.28864 | Thirteen LVLMs, nine TTS methods, and six benchmarks show capable small models can gain strongly, but extra tokens hurt several perception/hallucination tasks. Attention to image tokens decays after an early visual-encoding window, enabling plausible text-only drift. | Budget should be a controlled action with stopping, not a monotone “more is better” axis. Visual grounding can disappear even when the final reasoning trace grows. | §4 takeaways; Table 2; §6 attention/chain analysis; §7. |
| 2506.17417 | On RL-trained VLMs, majority voting consistently beats self-verified best-of-N; BoN gains are small and can drop by up to 16.7%; removing visual information changes verification little. | Apparent backtracking/verification language is not evidence of effective multimodal self-correction. Candidate diversity may dominate verifier quality. | Table 1 (p. 4); §4.1; §5–6. |
| 2512.05809 | MindJourney's verifier is poorly calibrated; random scoring can reduce entropy similarly and exposes action bias. ViSA's frame-anchored assertions help on SAT-Real, but every tested verifier plateaus on MMSI when imagined views add no reliable information. | Verification cannot repair an empty/low-fidelity candidate supply. Report information gain and random/equal-budget controls before attributing improvement to reward-guided selection. | Table 1 and §3.1; MMSI results; conclusion. |
| 2606.18323 | ASR best-of-N sharply reduces catastrophic TTS failure, but selection uses the target transcript. Authors explicitly call it a reference-aware oracle upper bound; the deployable path is a separately trained distilled model. A larger model resists, easy prose has no headroom, and distillation may regress near the floor. | The impressive selection result is excluded by test-item-gold access. Keep it as an audio supply/oracle/headroom control, never as strict self-verification occupancy. | Metric §3 (Whisper/WER); qualifications §4; distillation §5; conclusion. |
| 2605.28527 | Linear probes trained on outcome targets decode value-like structure from frozen VLA features. The online selector also uses simulator-backed candidate evaluation; authors characterize it as a diagnostic rather than a runtime controller. | “Frozen representation contains value” is not “deployment has a qualifying reward signal.” Probe training, outcome labels, and simulator access must stay visible. | §3.5 scope; Table 1/§4.2; §5 limitations. |
| 2606.08850 | Length-adjusted tail entropy ranks candidate sets and gates compute without a trained verifier; particle filtering/resampling extends this to step-level control. Its multimodal result uses a custom fine-tuned VLM on CAD, while most evidence is text/domain-general. | Useful verifier-free mechanism comparator, but multimodal-system proximity is element-level and should not be generalized to speech/omni occupancy. | §3–4; CAD analysis; §5 conclusion/limitations. |
| 2606.08231 | Survey taxonomy groups multimodal TTS into sampling-, feedback-, and search-based strategies. Its limitations explicitly say coverage is vision-language only and excludes audio/other sensory inputs. | Useful terminology/citation map, but neither an occupancy row nor evidence that the taxonomy covers native audio/omni control. | §§2–4; §7 limitations (p. 10). |

### Citation-triggered comparison paths

These four records were promoted only after their abstracts passed the same gate as the priority-queue
records. `2503.12271` is the sole citation-only discovery in this set; the other three independently occur in
the frozen BFS, so their citation edges corroborate proximity but do not receive extra recall credit.

| arXiv | System/control path | Boundary and mapping consequence | Full-text locator |
|---|---|---|---|
| 2503.12271 Reflect-DiT | A VLM judge critiques each generated image in natural language; the next diffusion generation conditions on a bounded sample of prior image/feedback pairs. The loop stops on null feedback or a fixed iteration cap. | This is not a training-free path: the Qwen2.5-VL judge, DiT, and added Context Transformer are fine-tuned on 78.5k synthetic image-feedback pairs. It is nevertheless a useful trained-feedback comparator for iterative state, feedback-conditioned candidate supply, and explicit stopping. Judge hallucination and small-object blindness remain inherited failure modes. | Algorithm 1 and §§3.1–3.3; §§4.1–4.2 training/sampling; §6 and Appendix B. |
| 2501.09732 Diffusion ITS | Search treats the initial noise or partial denoising path as the controllable candidate. Random search, zero-order local search, and path search are paired with privileged, conditional, self-supervised, or ensemble verifiers. | The diffusion generator remains pretrained, but most effective verifiers are external learned instruments; privileged-verifier results are upper bounds. The paper directly exposes verifier hacking and task-specific verifier bias, so it supports factorizing candidate supply, evaluator, and search allocation instead of treating “more inference compute” as one method. | Fig. 2 and §§3.1–3.2; §4.1 verifier construction; §7. |
| 2408.03314 Compute-Optimal TTS | Per-prompt difficulty selects how a fixed compute budget is split between parallel samples, sequential revisions, or process-reward-model tree search. | The key routing principle is adjacent, but the studied revision model and process verifier are capability-specifically fine-tuned; difficulty estimation is also model/task dependent. Gains shrink on the hardest problems, so adaptive allocation cannot create capabilities absent from candidate supply. | Fig. 1; §§4–7; §8 limitations. |
| 2407.21787 Repeated Sampling | A frozen generator independently samples candidates; automatic tests/proof checkers, majority vote, or reward models attempt final selection. The paper separates coverage (a correct candidate exists) from precision (the selector finds it). | It is the clean supply baseline and a direct adverse control: coverage can keep growing while majority/reward selection plateaus after roughly 100 samples. Hence a reward-guided controller must report both supply and selector quality, not only final best-of-N accuracy. | Fig. 1 and §1; §§2–4; §5. |

## Cross-paper deductions for the next coding pass

1. **Signal origin and action right must be joined.** Intrinsic uncertainty can drive attention, token,
   sample, tool, or stop decisions; identical words such as “verification” hide materially different edges.
2. **Supply/evaluator/controller effects are separable.** Random scoring, majority vote, stronger external
   judges, and missing-information plateaus repeatedly show that a better final result cannot be attributed to
   the controller unless candidate supply and evaluator strength are controlled.
3. **Training-free has at least four non-equivalent meanings:** no update to the base core; no update to the
   integration logic; no method-specific training anywhere; and no update plus no outside answer-bearing
   information. Only the last supports the strictest intersection.
4. **Native audio has two close white-box families in this round:** encoder-neuron activation control (IAAN)
   and uncertainty-gated contrastive token decoding (TCD). Audio generation reward search (SCORE/SMC-ITA)
   is structurally adjacent but uses external evaluators and a different task direction.
5. **Persistent system state is still rarer than repeated sampling.** LLM Orchestration has across-turn
   evidence-keyed memory; ImAgent and TTSP have within-item observation/knowledge state. Most decoding and
   best-of-N paths reset after the item and should not be counted as persistent controllers.
6. **Safety/stop is not implied by adaptive compute.** ImAgent exposes `STOP`; orchestration exposes
   cancellation/fallback; CORA exposes calibrated abstention. Many reward/search systems instead use a fixed
   budget without a safety right.
7. **Difficulty routing is bounded by capability and evaluator quality.** Compute-optimal allocation can
   choose among candidate-generation modes, but it does not repair an unproductive proposal distribution;
   repeated-sampling coverage likewise does not become deployable performance when the verifier cannot
   find rare correct candidates.

## Invalidating conditions

Revise a card if the local rendition/hash does not match its ledger receipt, an e-print supplies a conflicting
method detail, optional trained and untrained variants were accidentally merged, a second coder disputes a
load-bearing path, or a later paper changes the signal/action/information-boundary classification. Nothing in
this note authorizes an empty-intersection, novelty verdict, Stage-1C ranking, or research-model experiment.
