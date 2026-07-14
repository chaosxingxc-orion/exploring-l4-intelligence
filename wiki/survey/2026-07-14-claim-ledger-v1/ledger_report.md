# Claim Ledger v1 — Merge Report (P0-R3)

- **Date:** 2026-07-14
- **Status token:** `CLAIM_LEDGER_V1_SINGLE_PASS_AI`
- **generated_by:** `claim-ledger-v1 workflow, single-pass AI` (stamped on every ledger row)
- **double_review_pending:** `true` (stamped on every ledger row)
- **Ledger file:** `claim_ledger_v1.jsonl` (44 rows, one JSON object per line, sorted by `claim_key`; duplicate `claim_key`s are distinct rows for distinct papers and keep source order within the key)
- **Items dropped at extract stage:** 11 (dropped before this merge; NOT included in any count below)

## Review-status disclaimer (binding)

**Kills and occupancy verdicts in this ledger may NOT be written as final until human double
review (P1) completes.** This ledger is the output of a single-pass AI verification workflow
(`CLAIM_LEDGER_V1_SINGLE_PASS_AI`). Until P1 human double review signs off row by row, every
kill / occupancy / whitespace verdict herein is **direction-only** (hypothesis-grade): it may be
used to steer further survey work, but it must not be quoted as a settled verdict in any
owner-facing decision document.

All counts below are reported **separately, never aggregated** — in particular, the three
evidence grades must not be summed into any combined "verified" figure.

## Counts

**Total claims (ledger rows):** 44
(Note: rows = verified claim-instances; 40 unique `claim_key`s — `open-strict-i2-same-core` has 3 rows, `open-i3-combined-goodhart-speech` and `op-speechqe-hydraqe-trained-scorers` have 2 rows each. Row counts and unique-key counts are reported separately, not merged.)

### By evidence_grade (separate buckets — do not sum)

| evidence_grade | count |
|---|---|
| CLAIM_LOCATED_FULLTEXT | 35 |
| ABSTRACT_ONLY | 7 |
| FULLTEXT_UNREACHABLE_THIS_ROUND | 2 |

### By claim_class (explicit `claim_class` field only — absent field counted separately, not imputed)

| claim_class | count |
|---|---|
| (field absent in source row) | 34 |
| OPERATOR_CLASS | 5 |
| NUMERIC_HEADLINE | 4 |
| OCCUPANCY | 1 |

Informational only (NOT `claim_class`): claim_key prefix families — op=11, num=9, kill=7, open=7, occupy=5, reanchor=5. These are
name-family counts derived from the key string, kept separate from the `claim_class` field.

### By support_relation (separate buckets — do not sum)

| support_relation | count |
|---|---|
| SUPPORTS | 38 |
| LIMITS | 3 |
| RELATED_ONLY | 3 |

## P0-R7 operator census (operator_type × verifier_nature, row counts)

| operator_type \ verifier_nature | external-frozen | none | same-core | trained | unknown | row total |
|---|---|---|---|---|---|---|
| candidate-expansion | 1 | 0 | 0 | 0 | 0 | 1 |
| in-pool-selection | 9 | 3 | 3 | 2 | 0 | 17 |
| mixed | 0 | 1 | 1 | 4 | 5 | 11 |
| other | 0 | 4 | 1 | 3 | 0 | 8 |
| revision | 0 | 1 | 0 | 1 | 0 | 2 |
| tool-loop | 0 | 3 | 0 | 0 | 0 | 3 |
| weight-update | 0 | 0 | 1 | 1 | 0 | 2 |
| **column total** | 10 | 12 | 6 | 11 | 5 | 44 |

Notes:
- `mixed` marks rows whose paper (or paper-set) spans more than one operator class; see each row's `team_interpretation` / `numbers_note` for the split.
- `unknown` verifier_nature marks rows where the scorer/aggregator mechanism could not be verified this round (incl. the two FULLTEXT_UNREACHABLE rows).
- Marginal totals are provided for table readability only; they are not evidence-grade aggregates.

## Full discrepancy list (our artifact vs paper — verbatim; each entry is a candidate correction)

Every entry below reproduces the row's `discrepancy` field **verbatim** (both sides — our
artifact's statement and the paper's located text — are inside the quoted field as recorded by
the verification pass). Each non-empty entry is a **candidate correction** to our artifacts,
pending P1 human double review; none is applied to any upstream artifact by this merge.

Rows with non-empty discrepancy field: 43. Rows with empty discrepancy field: 1.

### D-01. `kill-goodhart-concept-text` — P-0080 (arXiv 2506.19248)

> Paper concerns MISSPECIFIED PROXY reward MODELS (learned), not 'verifiable reward' as team states - the over-optimization/N* result presumes reward imperfection; a truly verifiable reward is not the object. Selection is over a frozen POLICY's samples in a text-LLM setting, not audio/speech. Theorem numbering: HedgeTune characterization is Thm 3 (not Thm 1).

### D-02. `kill-i1-asr-st-mbr` — P-0071 (arXiv 2510.19471)

> Team's ~31% matches the LibriSpeech Table-9 figure specifically; the realization rate is dataset-dependent (ReazonSpeech ~9%). Paper reports no single blended ~31% across 'LibriSpeech/FLEURS/CoVoST families'; FLEURS/CoVoST oracle gaps not located verbatim this round.

### D-03. `kill-i1-i2-audio-understanding` — P-0031 (co-leads P-0032/2603.09714, P-0036/2501.07246) (arXiv 2503.23395)

> scaling-auditory headline numbers match exactly (36.7->50.0/40.0->66.7, +36.2%/+66.8%, 9-150%). MUGEN K=10 and Audio-CoT '5-sample' counts not located verbatim (methods/gains confirmed). Co-lead numbers via fulltext-search snippets, not direct fetch.

### D-04. `kill-i1-i2-ser-jia` — P-0005 (arXiv 2602.03873)

> All three team numbers match the Qwen2-Audio table; team cites CREMA-D 51.26 (ALM-v column) though W-BoN peaks higher at 53.24. Team's K=3-5 sample count not located verbatim (BoN described as beam-search-based).

### D-05. `kill-i3-abstain-audio-understanding` — P-0034 (arXiv 2604.25591)

> Team 'AUROC 0.84-0.85' vs paper semantic-entropy MMAU 0.82-0.84 (max ~0.84); team 'AURAC 0.73-0.92' vs paper 0.73-0.95; team 'P(True) 0.79'=low end of AQUA-Bench 0.79-0.89. Also semantic-entropy (the top method) uses an external NLI clustering step, so verifier is partly external-frozen not purely same-core.

### D-06. `kill-i3-conformal-asr-ernez` — P-0062 (arXiv n/a)

> Material mischaracterization: team says 'WER<2% at 80% coverage' but the paper's 80% is a CONFIDENCE/guarantee level, not an answer-coverage rate; the risk guarantee holds for a prediction SET averaging 29 sentences, not for a single-output selector answering 80% of the time. Calibration uses gold labels on the LibriSpeech clean-test SPLIT (~2,600 sentences), not on the test item itself. It is a conformal risk-controlled set-prediction/abstention method, not a single-output reward-guided selector.

### D-07. `kill-rho-metric-prior-art` — P-0039 (arXiv 2603.12520)

> Abstract fully supports the headline numbers (r=0.47; 21.0%->61.2%; Chatbot Arena best-of-4). But (a) paper's Recovery is anchored to RANDOM choice (=pool mean) so it formalizes our rho_pool specifically, not rho_greedy (deployment-default anchor); team's 'formalizes our rho' should be narrowed to rho_pool. (b) Paper uses 21.1% (not team's 21.0%) as the pairwise-recovery baseline. (c) The exact algebraic formula was not located (only the abstract's prose definition was reachable).

### D-08. `num-audio-mind-f3-goodhart-cliff` — P-0035 (arXiv 2605.28480)

> Our line states a 'Goodhart cliff beyond ~10 tool calls' as fact; the paper reports degradation on only SIX questions in the >10-call bucket (50.0% -> 16.7%) and explicitly 'treats conclusions cautiously due to limited examples' -> n=6 signal, not a robust cliff. Also baseline is named 'Qwen3.5-Omni' (unusual/possibly mis-parsed model name).

### D-09. `num-autagent-oracle-ceiling` — P-0065 (arXiv 2602.13685)

> This is TOOL-selection headroom on an RL-TRAINED (GRPO, Baseline-Subtracted Differential Reward) policy — NOT a frozen-omni K-sample-pool oracle; artifact correctly flags this. Note: GPT-4o baseline is 57.40 (not 50.0), so expressing its +9.80 as '61% of the 16.1-pt ceiling' (a ceiling anchored to a 50.0 baseline) is a loose ratio. Frozen-omni audio-understanding K-pool oracle/rho stays unmeasured (artifact's stated gap holds).

### D-10. `num-iad-loop-vs-bon-bar` — P-0094 (arXiv 2504.01931)

> Gains are dataset-dependent: ≈3-4% is the Sketch2Code/Text2SQL figure; WebShop reaches 8-10% (abstract 'up to 10%'). Artifact's 'only ~3-4 pts' is the conservative low end — defensible but understates WebShop. Intercode: fetched v1 reports NO Intercode experiment (census note lists 'Sketch2Code/Text2SQL/Intercode/WebShop' — Intercode may be a later-version addition; flag). 'Front-loaded rounds 1-2' CONFIRMED (Fig 5b BON ceases after 2 iters; per-N margin decays 3.33→1.95→1.00).

### D-11. `num-kit-per-task-oracle-realized` — P-0084 (arXiv 2606.04730)

> ST oracle is +6.11 COMET, NOT +2.0 as the artifact states — numeric error, and 'ST headroom small but nonzero' mischaracterizes +6.11. ASR -32.1 / SQA +14.4 / SSUM +3.9 match exactly (confirms census-AMBIGUOUS P-0084 = 2606.04730). CRITICAL OMISSION: label-free realization is NEGATIVE on SQA (Lik -11.06 / +MBR -3.33) and SSUM (-8.60 / -2.19) — the selectors HURT vs baseline; only ASR realizes a positive fraction (77.6% / 60.0%), ST near-zero. Artifact's 'fraction realized across 4 speech tasks' framing overstates a mostly-negative result.

### D-12. `num-li2020-slu-headroom` — P-0008 (arXiv 2001.05284)

> Two: (1) our line headlines it 'SLU-intent' but the 27.04%/14.29% figures are DOMAIN classification RErr (Table 3); the intent-classification figures are 11.92-25.55% (Table 6). (2) 'oracle' = ground-truth-transcription upper bound (clean-input read-out), not a best-of-pool/N-best selection oracle as the surrounding headroom sections imply.

### D-13. `num-ma2024-asr-headroom` — P-0044 (arXiv 2409.09554)

> Minor: our line says 'beam 5/10-best'; paper says '5-best/10-best list' (N-best). More important: oracle (in-pool best-of-N) and realized (trained generative EC that can produce out-of-pool text) are different operator classes collapsed into one headroom line.

### D-14. `num-mbr-asr-flagship-rho-gap` — P-0071 (arXiv 2510.19471)

> Claim's 'Ja-En 8.08' is the MBR N=64 value (paper 8.078); artifact omits the Ja-En beam baseline 6.218 (it does give En-Ja beam 8.242). Minor incompleteness only — the 31% rho, LibriSpeech 4.2→3.3 vs oracle 1.3, and En-Ja 8.24→11.68 are all exactly confirmed.

### D-15. `num-novosad-rho-collapse` — P-0043 (arXiv 2606.23306)

> Material: (1) our 'rho collapse (realizable fraction does not grow)' holds only for CTC-INTERNAL/acoustic scoring; the paper's main result is that frozen RoBERTa PLL rescoring DOES break through (5.42% vs 5.96%, 9.0% rel) -> headroom is partly realized. (2) The paper's 'rho' is Spearman rank correlation, NOT our realization-rate rho (same-name-different-meaning per glossary). (3) 'our librispeech' -> this is the PAPER's LibriSpeech (Zipformer-S CR-CTC), not an in-house pool. (4) Census tags it 'kills I2/I4' while the neighbor-matrix cell frames it as a PARTIAL ancestor.

### D-16. `num-siskos-supply-conditional-asr` — P-0050 (arXiv 2509.19567)

> Wording precision: our line says 'realizes ~69-77% of oracle WER'; it is ~69-77% of the oracle WER IMPROVEMENT (fraction of headroom closed), not of absolute oracle WER. Also the 'oracle' is a supply upper bound (ground-truth words), a new-info lever, not a pool-selection oracle.

### D-17. `occupy-aac-mechanism-slam-aac` — P-0023 (arXiv 2410.09503)

> Minor: team labels it 'frozen CLAP cosine' (true for the VERIFIER) but the caption-generation LLM is LoRA fine-tuned (not fully frozen) — only the CLAP selector is frozen/external. Team's own neighbor-matrix already tags this 'mixed/FT' and the kill note concedes 'not our datasets', so no substantive conflict, but the selection is over a LoRA-trained generator's outputs.

### D-18. `occupy-i3-conformal-ser-trained` — P-0004 (arXiv 2503.22712)

> Discrepancy in team parenthetical 'gold at inference': the paper's coverage guarantee relies on gold labels at CALIBRATION (a labeled calibration set → quantile), then constructs prediction sets on UNLABELED test samples — the test item's own gold is NOT consumed at inference. 'gold at inference' overstates/mislabels; should read 'gold at calibration'. Matters for the information-boundary framing.

### D-19. `occupy-supply-type-analogy-only` — P-0087; P-0085 (arXiv 2606.29947 (ColdStart); 2408.15240 (GenRM))

> GenRM does NOT present an explicit 'realized-fraction-of-Pass@N grid' as the artifact states; it shows Fig 5 (GenRM-CoT ≈ oracle-verifier BoN) plus BoN-vs-baseline deltas, not a fraction-realized grid — mild overstatement of GenRM's actual presentation. Both papers are text (GenRM) / recsys (ColdStart) only; no speech/omni occupant, so the I4 whitespace verdict itself holds.

### D-20. `occupy-text-training-free-rl` — P-0091;P-0092;P-0066 (arXiv 2303.11366;2510.08191;2601.18510)

> None material. All three are confirmed text / text-agentic (WebArena, Jericho, tau2-bench, HumanEval, math/web-search) — supporting the team's explicit 'all text' framing. JitRL's 'closed-form KL-constrained solution' matches the project-thesis mechanism verbatim.

### D-21. `occupy-umbrella-system-audiotoolagent` — P-0064 (arXiv 2510.02995)

> None material — all three benchmark numbers match the abstract exactly. Verifier framing (agent arbitrates, no reward signal selecting) is consistent with the paper's 'without accessing the audio' tool-orchestration.

### D-22. `op-aqa-ttrl-weights-change` — P-0033 (arXiv 2510.05478)

> None. Confirms weight-updating (fine-tune ALL parameters), test-time GRPO, majority-vote/self-consistency pseudo-labels, on MMAU/MMAR/MMSU. Base model is Qwen2.5-Omni (consistent with our cross-card notes).

### D-23. `op-audiotoolagent-no-audio-access` — P-0064 (arXiv 2510.02995)

> None material. 'Agent does not access audio directly' confirmed verbatim; tool-orchestration (ReAct) vs K-pool selection confirmed. Refinement for census: the operator is a TOOL LOOP (iterative follow-up calls, output comparison, self-verification by re-invoking tools with different inputs), not single-pass orchestration - pool_changed=yes because the candidate/evidence set is expanded through successive tool calls, not selected from a fixed K-pool.

### D-24. `op-autagent-trains-grpo-adversary` — P-0065 (arXiv 2602.13685)

> Nuance, not contradiction: paper FREEZES the reasoning backbone; only the separate tool-selection policy is GRPO-trained. Our 'not weight-frozen overall' holds only for that policy head, not the reasoner. Reward is a ternary 'Baseline-Subtracted Differential Reward', not plain accuracy. Selection is single tool from a fixed pool of 6 (no chaining), tool output can override the frozen reasoner's baseline answer -> candidate set expands.

### D-25. `op-jia-external-gpt4o-no-oracle` — P-0005 (arXiv 2602.03873)

> TWO discrepancies with 'text-side' and 'fixed beams': (1) the ALM verifier 'receives the audio input and each of the B responses' - so GPT-4o is given the audio, not purely text-side (though still EXTERNAL GPT-4o, not the self-contained frozen-omni core, so the core distinction survives). (2) Beam is 'optimized within [2,7]' (B=5 BoN, B=3 ALM-v) - tuned within a range rather than strictly fixed. The no-oracle / rho-UNKNOWN / no-Goodhart / I3-I4-open conclusions hold.

### D-26. `op-kit-lora-not-frozen` — P-0084 (arXiv 2606.04730)

> MAJOR mismatch vs our artifact on 3 of 4 asserted details. (1) TASK COUNT: our 'four tasks' vs paper's SIX. (2) RERANKING MODALITY: our 'reranking scores are text-only' is WRONG — the PRIMARY reranker is AUDIO-GROUNDED (Qwen2.5-Omni conditions on audio); text-only is only the secondary/contrastive Whisper+Gemma path. (3) ARCHITECTURE: our 'Whisper->LoRA-LLM->TTS cascade' is WRONG — primary is Qwen2.5-Omni END-TO-END audio-direct with LoRA; ASR (parakeet) appears only in the contrastive cascade; TTS (Kokoro-82M) is only synthetic-data generation, not the pipeline. Only 'LLM is fine-tuned, NOT weight-frozen' (LoRA rank 32) is confirmed. Census flagged P-0084 AMBIGUOUS — our artifact may have mischaracterized 2606.04730 or intended a different KIT paper.

### D-27. `op-mbr-asr-text-only-decision` — P-0071 (arXiv 2510.19471)

> None material. Paper confirms text-only BLEU utility and explicitly refuses WER/audio at the decision step, matching our claim exactly. (verifier_nature marked 'none' because scoring is a text-overlap metric over same-core samples, not a separate verifier model.)

### D-28. `op-read-external-tts` — P-0075 (arXiv 2606.04680)

> None material. Headline 2.06->1.91 and 'frozen external TTS, no additional training' both confirmed. Minor note: beyond the sentence-level rescoring that produces the headline number, the paper also does segment-level combination + ROVER (a mild recombination beyond pure in-pool selection), so the method is not purely single-pass selection.

### D-29. `op-scaling-auditory-external-verifier-no-rho` — P-0031 (arXiv 2503.23395)

> DISCREPANCY on 'fixed temp/beam': the paper actually SWEEPS temperature 0-2 (increments 0.2, for majority voting) and beam count 2-7 (Appendix B.2), i.e. it varies decoding/supply params rather than holding them fixed. The load-bearing conclusions (external GPT-4o verifier; no oracle/rho/regret/abstention/Goodhart; non-benchmark tasks; I4 open) still hold, but the 'fixed temp/beam' descriptor in our artifact is inaccurate. Also: verifier is 'chosen as the one with superior audio comprehension' (GPT-4o, audio-capable) - external, not same-core.

### D-30. `op-speechqe-hydraqe-trained-scorers` — P-0017 (arXiv 2410.21485)

> None at abstract level; aclanthology.org fulltext blocked this round (domain-safety block), so numeric internals unverified. Abstract fully supports 'trained/fine-tuned QE scorer, not a frozen selector'.

### D-31. `op-speechqe-hydraqe-trained-scorers` — P-0018 (arXiv 2606.08748)

> NUMERIC: our artifact states HydraQE seg-level = 29.8; the located Table 3 test-set average is 29.1 (still > gold-transcript CometKiwi 28.5). DIRECTION confirmed (HydraQE > gold-transcript CometKiwi), but the exact figure differs — 29.8 not found; likely a different split/language-pair/submission column. Also: paper confirms HydraQE SCORES only, does NOT select/rerank a pool, matching 'not a frozen selector'.

### D-32. `op-walking-uncertainty-not-reward-guided` — P-0034 (arXiv 2604.25591)

> None material. Minor: metrics are AUROC AND AURAC (our artifact says 'AUROC/token-savings' — AURAC additionally present, no conflict). Paper's own caveat 'uncertainty alone is not sufficient to guarantee better routing decisions' is a routing-quality limitation, NOT a Goodhart/reward-hacking framing.

### D-33. `open-i3-combined-goodhart-speech` — P-0080 (arXiv 2506.19248)

> None — abstract confirms the paper is text-LLM-only with no speech/audio, directly supporting the team's claim that Goodhart/over-optimization detection is 'owned only in text.'

### D-34. `open-i3-combined-goodhart-speech` — P-0034 (arXiv 2604.25591)

> None material — confirms selective-prediction/abstention on frozen ALLMs via uncertainty is occupied, but the paper does NOT detect Goodhart/reward-hacking nor characterize a rho realization surface, consistent with the whitespace for the COMBINED selector.

### D-35. `open-i4-realization-surface` — P-0084 (arXiv 2606.04730)

> Supports 'partial ancestor only': KIT TRAINS (not frozen) on 1M augmented instances and does NOT characterize any supply-conditional rho/H/regret surface; its inference-time part is fixed-pool best-of-N re-ranking (likelihood + MBR). Note: census flagged P-0084 as AMBIGUOUS between arXiv 2606.04730 (long-form instruction, fetched here — best fit for the 'supply/long-form' framing) and 2606.07240 (voice cloning); this row verifies 2606.04730.

### D-36. `open-strict-i2-same-core` — P-0075 (arXiv 2606.04680)

> None — abstract verbatim confirms READ scores hypotheses with an EXTERNAL pretrained TTS model (not the generating ASR/omni core), directly supporting the whitespace claim that I2 occupants use external scorers.

### D-37. `open-strict-i2-same-core` — P-0031 (arXiv 2503.23395)

> Could NOT verify the artifact's 'external GPT-4o scorer' attribution: arxiv HTML/PDF socket-closed on every attempt, HuggingFace mirror 404'd, and the reachable abstract does not mention GPT-4o or any scoring/aggregation mechanism. Paper identity and topic (test-time compute on frozen audio LLMs, 5 TTC methods) are confirmed; the scorer-nature claim is UNVERIFIED this round.

### D-38. `open-strict-i2-same-core` — P-0005 (arXiv 2602.03873)

> Could NOT verify the artifact's 'external GPT-4o scorer' attribution: arxiv HTML/PDF socket-closed, HuggingFace mirror 404'd, and the reachable abstract confirms only the benchmark setup (8 ALMs, 5 TTS strategies, 3 SER datasets) with no mention of GPT-4o or the aggregation mechanism. Paper identity confirmed; scorer-nature claim UNVERIFIED this round.

### D-39. `open-umbrella-intersection` — P-0064;P-0031;P-0091;P-0092;P-0066 (arXiv 2510.02995;2503.23395;2303.11366;2510.08191;2601.18510)

> *(empty discrepancy field in source row — no discrepancy recorded)*

### D-40. `reanchor-coordinator-verified-depth-cap` — P-0071,P-0075,P-0031,P-0064,P-0005 (arXiv 2510.19471; 2606.04680; 2503.23395; 2510.02995; 2602.03873)

> The header ITSELF already qualifies the label ('personal WebSearch this session'), so CL-0118's downgrade is warranted. The overclaim risk materializes downstream: decision-package L11/L39 propagate the bare 'COORDINATOR-VERIFIED' WITHOUT the 'personal WebSearch' qualifier, and its evidence_grade field reads '5 load-bearing kills COORDINATOR-VERIFIED' — which reads as claim-verified. Also note the original coordinator pass has no page/table locator (RAW_EVENT_UNAVAILABLE), so its recorded depth cannot be independently inspected.

### D-41. `reanchor-mbr-asr-scorer-identity` — P-0071 (arXiv 2510.19471)

> Superseded sota-cards-v2 F2 column welded 'Whisper-lv3 + Llama-3 scorer' to the MBR WER, implying an LLM produces the MBR number — WRONG per paper (MBR utility is BLEU/sacrebleu; Llama-3 appears only in the ProGRes baseline). Minor locator imprecision in our CL-0115: it cites 'Tables 6/7' for beam/MBR, but the Beam/MBR/Oracle triple I located is in Table 1; values match regardless.

### D-42. `reanchor-progres-candidate-expansion` — P-0042 (arXiv 2409.00217)

> Ledger internal inconsistency CONFIRMED: papers.jsonl P-0042 records strengths [row 44 audio-judge-multi = PARTIAL, row 78 kill-I1 = DIRECT], 'strength_conflict': true, grade_effective ABSTRACT_VERIFIED. NOTE: CL-0117's source_artifact_refs cite neighbor-matrix-v2 L84/L138 as the conflicting rows, but BOTH neighbor-matrix rows read DIRECT — the real PARTIAL/DIRECT split lives in scout-ledger/papers.jsonl (rows 44/78), so the artifact-ref pointer is slightly mislocated though the conflict itself is genuine.

### D-43. `reanchor-read-realized-fraction` — P-0075 (arXiv 2606.04680)

> The superseded '~70-85% oracle realized' (neighbor-matrix-v2 L147, coverage-and-kill-matrix-v2 L24) is CONTRADICTED by Table 1: only TALCS 67.5% and SWBD 68.5% approach that band; the 8-dataset span is 7.7–68.5% and LibriSpeech is 11.9–16.5%. No discrepancy between our CORRECTED numbers and the paper. Paper's external model is specifically CosyVoice2 (our artifact says generic 'external TTS' — consistent, just less specific).

### D-44. `reanchor-tap-ger-out-of-pool` — P-0072 (arXiv 2309.15649)

> The abstract states below-oracle rates come 'By combining prompting techniques with fine-tuning,' yet Table 3's FROZEN InstructGPT+TAP row (8.72) already beats the 9.78 n-best oracle on WSJ — so sub-oracle is reachable frozen (via generation), not only via fine-tuning. This does not contradict our correction; it confirms the operator is generative (out-of-pool). The load-bearing numbers 8.72/9.78/8.41/29.56/11.87 all match our CL-0116 corrected text.

---

Status: `CLAIM_LEDGER_V1_SINGLE_PASS_AI` — single-pass AI merge; human double review (P1) pending;
kills/occupancy verdicts direction-only until then.
