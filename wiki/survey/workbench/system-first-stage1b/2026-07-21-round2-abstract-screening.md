---
title: "Stage-1B round-2 abstract screening and full-text promotion"
date: 2026-07-21
stage: "STAGE_1B_SYSTEMATIC_MAPPING"
role: "WORKBENCH D1 decisions; not canonical REC-0 completion or a novelty verdict"
---

# Stage-1B round-2 abstract screening and full-text promotion

## Queue and decision boundary

The deterministic queue builder ordered 20,696 D0 candidates not named in the opening workbench notes
and wrote the first 120 records to the external data store. The JSONL SHA-256 is
`5cdba4e4e06109374e5f1c9099140b721d53a902faf6ee9a2a8804d2041bacb3`. Its lexical score is only a
review order: every row remained `ABSTRACT_REVIEW_PENDING`, and the builder made zero screening
decisions. Six protocol blind-spot sentinels were forced to the front with
`query_recall_credit_for_forced_entry=false`; all six were also independently present in the frozen
arXiv-query union, so their original query lineage remains visible.

This round manually reviewed the abstracts below. `SELECT_FULLTEXT` means that the abstract shows a
direct system/control path, an adverse/limit result needed to prevent favorable-only synthesis, or a
load-bearing measurement/taxonomy role. It authorizes acquisition, not acceptance of the paper's
claims. `DEFER` retains the item in the DFS queue. `ABSTRACT_EXCLUDE` is used only when the abstract
establishes a wrong object or a training-only path with no load-bearing inference-time element.

## D1 decisions

| arXiv | Priority | Abstract-level decision | Why this decision is warranted before download |
|---|---|---|---|
| 2512.19433 | P0 | SELECT_FULLTEXT | A single diffusion MLLM performs hierarchical trajectory search and intrinsic text-image self-verification; direct self-signal-to-selection/stopping path. |
| 2512.11109 | P0-negative | SELECT_FULLTEXT | Cross-model/benchmark study reports external verification as the reliable gain while iterative self-refinement may degrade; needed adverse control. |
| 2606.08231 | P2-lineage | SELECT_FULLTEXT | Dedicated multimodal TTS survey with sampling/feedback/search taxonomy; useful for citation expansion and terminology cross-check, not occupancy by itself. |
| 2606.28864 | P0-negative | SELECT_FULLTEXT | Frozen-weight LVLM study reports task/model-size dependence, loss of visual focus under excess compute, and early collapse to text-only reasoning. |
| 2602.23306 | P0 | SELECT_FULLTEXT | Training/data-free omni decoding controlled by an external LRM and stepwise contrast; direct topology and external-guidance boundary case. |
| 2508.10016 | P0 | SELECT_FULLTEXT | Training-free multimodal expert orchestration exposes explicit routing tokens, persistent cross-modal memory, sequencing, and streaming/interruption rights. |
| 2510.13804 | P1/P2 | SELECT_FULLTEXT | A separately trained omni-capable verifier drives sequential refinement; essential external-component and verifier-attribution comparator. |
| 2603.16253 | P0-negative/P2 | SELECT_FULLTEXT | Claims visual PRM scores entangle perception errors with reasoning errors; directly tests whether a reward signal is causally trustworthy. |
| 2511.11483 | P0 | SELECT_FULLTEXT | Training-free unified multimodal agent integrates generation, self-evaluation, and policy-controlled actions without external models. |
| 2508.11616 | P1-direct | SELECT_FULLTEXT | Reward-guided decoding of MLLMs is a direct signal-to-token-action path, with a trained grounding reward model that must be separated from strict occupancy. |
| 2606.18323 | P0-audio/negative | SELECT_FULLTEXT | ASR round-trip best-of-N self-verification removes catastrophic TTS failures, while distillation and a resistant model expose attribution/headroom limits. |
| 2606.08850 | P1 | SELECT_FULLTEXT | Intrinsic sample statistics replace trained/exact verifiers and control selection, resampling, and difficulty-gated compute; useful verifier-free comparator. |
| 2602.04208 | P0 | SELECT_FULLTEXT | Claims training-free uncertainty-conditioned re-observation and execution for VLAs, directly linking uncertainty to look/act rights. |
| 2510.05681 | P0 | SELECT_FULLTEXT | Verifier-free VLA selection uses the base policy's own masking distribution; direct endogenous-signal comparator. |
| 2506.17417 | P0-negative | SELECT_FULLTEXT | Explicitly tests whether VLMs can self-verify and self-correct under inference-time scaling; adverse result can falsify generic self-refinement claims. |
| 2509.19831 | P0-audio | SELECT_FULLTEXT | Training-free multi-reward guidance controls text-to-audio generation and exposes composite-reward calibration/attribution. |
| 2604.12647 | P0-audio/boundary | SELECT_FULLTEXT | Confidence routes respiratory audio through progressively richer stages and early exit; retrieval at the highest tier tests information-boundary sensitivity. |
| 2504.11101 | P0/P1 | SELECT_FULLTEXT | Training-free inter-model consensus entropy verifies, selects, and adaptively routes OCR outputs; same-cost and VLM-judge controls are promised. |
| 2607.11801 | P0-audio | SELECT_FULLTEXT | Training/label-free intervention identifies and amplifies audio-encoder neurons; strong native-audio, white-box, inference-control boundary case. |
| 2601.05159 | P0 | SELECT_FULLTEXT | Training-free vision-language introspection diagnoses conflicts and applies instance-specific latent steering; direct internal-state/control path. |
| 2512.05809 | P0-negative | SELECT_FULLTEXT | Finds random scoring can match a world-model verifier, exposes action bias, and reports an information bottleneck where no tested verifier scales. |
| 2606.08393 | P0-audio | SELECT_FULLTEXT | Sequential Monte Carlo search reallocates video-to-audio compute using multidimensional rewards and matched-budget comparisons. |
| 2605.28527 | P1-boundary | SELECT_FULLTEXT | Reads value-like success information from a frozen VLA with lightweight probes and uses it for action choice; separates pretrained readout from trained controller. |
| 2604.15383 | P0-audio | SELECT_FULLTEXT | Training-free temporal contrastive decoding uses original/blurred audio views, logit control, and an uncertainty/audio-reliance gate. |
| 2604.11025 | P0 | SELECT_FULLTEXT | Treats perception as a test-time search space with tools and addresses the circular "where to look" grounding problem. |
| 2604.09155 | P0-safety | SELECT_FULLTEXT | Post-policy conformal risk controller can block/redirect GUI actions and supplies a stopping/safety counterpoint to capability-only loops. |
| 2506.17811 | P1 | DEFER | Strong VLA sampling/verifier path, but the verifier is separately trained and the current batch already contains less redundant VLA control paths. |
| 2509.02129 | P1 | DEFER | Zero-shot MLLM TTS for visual place recognition is relevant but task-specific; retain behind general controller and adverse-control papers. |
| 2605.24785 | P1 | DEFER | Multimodal web-agent efficiency and skill accumulation are relevant, but online distillation moves the principal object outside strict no-update control. |
| 2603.14724 | P1 | DEFER | The reflection controller is real but bound to a game-UI/Figma pipeline; retain as a domain implementation comparator. |
| 2603.00141 | P1 | DEFER | Adaptive verification/pruning/stopping for image editing overlaps the selected general image-generation control paths. |
| 2602.07399 | P1 | DEFER | Value-guided VLA action-chunk selection depends on a fine-tuned policy and trained critic; keep for the trained-controller stratum. |
| 2506.07971 | P1 | DEFER | Cybernetic video self-monitor/correction is relevant, but detailed reading follows the more direct speech/omni and negative batches. |
| 2510.10975 | P1 | DEFER | Robot PRM verifier is a close comparator but redundant in this round with selected VLA endogenous-signal and perception-scaling papers. |
| 2604.24583 | P2 | DEFER | Perception-centric PRM is trained and primarily used for RL; its repeated inference repair path remains eligible for the verifier stratum. |
| 2507.07424 | P1 | DEFER | Self-verification is attached to a newly trained MLLM; retain for later trained-backbone sensitivity analysis. |
| 2604.17175 | -- | ABSTRACT_EXCLUDE | Protein sequence design is the operative object; the multimodal lexical hit does not create speech/omni/system-control proximity. |
| 2603.12149 | -- | ABSTRACT_EXCLUDE | The proposed confidence reward is used for reinforcement-learning training, not a qualifying frozen inference-time controller. |
| 2606.24231 | -- | ABSTRACT_EXCLUDE | Reward-conditioned driving planning is learned during training; test-time sampling is not the paper's load-bearing system-control contribution. |
| 2603.16805 | -- | ABSTRACT_EXCLUDE | Multi-stream watermarking/separation is a trained signal-processing pipeline without the target frozen-model inference-control object. |

## Acquisition batch

The 26 `SELECT_FULLTEXT` IDs are the only new full-text-authorized items in this note. Acquisition must
use `scripts/survey/sf_fulltext_fetch.py`; PDF and e-print stay under the external survey store, while
Git retains URLs, byte counts, SHA-256 receipts, this abstract rationale, and later D2 notes. Existing
local copies are re-hashed rather than fetched again. No full-text claim is accepted until the local
rendition is opened and a locator-backed D2 note is written.

## Citation-triggered abstract pass

An offline arXiv-ID pass over the first 16 locally opened round-2 texts found 410 distinct cited arXiv
IDs. Frequency alone was not treated as relevance: the most common IDs were backbone/model reports
(`2410.21276` GPT-4o, `2312.11805` Gemini, `2502.13923` Qwen2.5-VL, `2505.09388` Qwen3), datasets,
or training papers and were registered as background rather than expanded. The following method/comparison
edges independently satisfied a DFS trigger after their abstracts were inspected:

| arXiv | Citation role | Abstract-level decision | Reason |
|---|---|---|---|
| 2503.12271 | backward method lineage from four image-TTS nodes | SELECT_FULLTEXT | Reflect-DiT replaces passive best-of-N with image-plus-text-feedback reflection and reports a matched sample-efficiency contrast. |
| 2501.09732 | backward comparison from image/audio generation nodes; also frozen-query hit | SELECT_FULLTEXT | Frames diffusion inference scaling as verifier × search-algorithm design, directly exposing candidate-supply and evaluator interactions. |
| 2408.03314 | backward comparison from five nodes; also frozen-query hit | SELECT_FULLTEXT | Compute-optimal allocation uses process verifier search/adaptive distribution updates and reports strong prompt-difficulty dependence. |
| 2407.21787 | backward comparison from five nodes; also frozen-query hit | SELECT_FULLTEXT | Repeated-sampling study reports that reward-model/majority selection plateaus without automatic verification, a load-bearing supply-versus-selector control. |

These four are a separate citation-trigger acquisition tail. Their citation provenance does not replace the
independent frozen-query entrance for the three already present in BFS, and no generic backbone/dataset
reference is expanded merely because it is common.
