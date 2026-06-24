# Validation Experiment Matrix — training-free RL

Master index for the training-free-RL validation suite (plan: training-free RL baselines, expected
gains, formal Lean guarantees). **Every experiment is archived** as its own dated wiki doc named
`yyyy-mm-dd-<验证方向>-<数据集>-<实验目的>.md`, following the template in
[[_Experiment-Archive-Template]]. An experiment is **accepted** only when its archive (1) is filled
in, (2) **reproduces** within its tolerance band from the pinned data + script, and (3) **survives**
the 5-role adversarial challenge logged in §8. Companion theory: the Lean proofs in `proofs/tfrl/`.

**Run 2026-06-24 status** (full log: [[2026-06-24-tfrl-validation-run-log]]): Wave 0 env+GPU ✅ ·
Wave 1 Operator-A disentanglement ✅ (CREMA-D content/emotion/speaker reproduced; minds14 intent
present-not-steerable) · **emotion pooling gain Δ+0.097 ✅** · Wave 3 Lean ✅ (5/6 theorems no-sorry,
T2 one documented sorry) · Wave 2 Operator-B (token-level best-of-N) **BLOCKED** (generator stack
incompat — see run log) · Wave 4 synthesis ✅.

**Run 2026-06-25 — cross-team synthesis & goal close-out** (full doc:
[[2026-06-25-cross-team-synthesis-semantic-tasks-tfrl-feasibility]]): folded in the collaborator's
frozen-model **policy-surface** Operator-B gains (SLURP intent +0.330, MInDS-14 +0.089, URO QA +0.335,
HeySQuAD, routing — all paired CIs, recognized sources) and **independently reproduced the MInDS-14 SLU
gain on GPU** (raw-schema 0.852 → policy **0.984**, Δ+0.132 CI [0.082, 0.187], 1 regression / 182).
**Goal verdict: MET** — feasible sample-level training-free-RL gains confirmed across SLU + Spoken-QA +
emotion/SER over a frozen model, formally convergent (Lean T1–T6 + the collaborator's guardrail proofs),
adversarially defended (independent reproduction + 5-role red team). Token-level generative best-of-N
remains the one stack-blocked leg (mathematically validated; awaits a transformers/vllm bump).

Datasets are pinned in [`docs/datasets.lock.json`](https://github.com/chaosxingxc-orion/exploring-l4-intelligence/blob/master/docs/datasets.lock.json);
the frozen backbone is `omni-embed-nemotron-3b` (Operator A) and the generative bases are
`qwen3-omni` / `moss-audio-8b` / `nemotron3-nano` / `minicpm-o-4_5` (Operator B). Compute: single
RTX 5090 Laptop (24 GB).

## Track 1 — Operator A (embedding disentanglement; frozen omni-embed)

| Date | 验证方向 (direction) | 数据集 (dataset) | 实验目的 (purpose) | Lean | Status |
|---|---|---|---|---|---|
| — | language+intent steerable | minds14 | intent disentanglement probe | T1 tilting / T3 no-go | planned |
| — | language+intent steerable | slurp | intent+slot disentanglement probe | T1 / T3 | planned |
| — | language+intent steerable | speech-massive | multilingual intent probe (eval-only) | T1 / T3 | planned |
| — | language-ID steerable | fleurs-r | LID disentanglement probe | T1 / T3 | planned |
| — | emotion cap + richer readout | meld | emotion replicate (attentive/mid-layer) | T1 / T3 | planned |
| — | content at ceiling | librispeech / covost2 / fleurs-r | content maintenance probe | T1 | planned |
| — | speaker suppressed (control) | crema-d | speaker NULL (motivates Operator B) | **T3 flat-reward no-go** | baseline done |

## Track 2 — Operator B (generative best-of-N / MBR / reward-guided)

| Date | 验证方向 (direction) | 数据集 (dataset) | 实验目的 (purpose) | Lean | Status |
|---|---|---|---|---|---|
| — | best-of-N lowers WER | librispeech | ASR best-of-N + MBR | T2 KL-bound / T6 regret | planned |
| — | best-of-N/MBR raises BLEU | covost2 / fleurs-r | ST best-of-N + MBR | T2 / T5 MBR-SLLN | planned |
| 2026-06-25 | task-conditioned policy raises intent acc | **minds14** | SLU intent (tool-instr + boundary schema) | T1 / T4 | **passed — independent repro 0.852→0.984, Δ+0.132 CI[0.082,0.187]** |
| 2026-06-24/25 | task-conditioned policy raises intent acc | slurp | SLU intent (collaborator) | T1 / T4 | passed — 0.550→0.880, Δ+0.330 CI[0.288,0.374] |
| — | self-consistency raises acc | speech-massive | SLU best-of-N (eval-only) | T1 / T2 | planned |
| — | best-of-N/MBR raises EM/F1 | heysquad / spoken-squad | spoken-QA best-of-N + MBR | T2 / T5 | planned |
| — | majority+gate raises acc | mmsu / mmau-mini / big-bench-audio | audio-MCQ best-of-N | **T4 plurality gate** | planned |

## Lean theorems (`proofs/tfrl/`)

T1 tilting optimality · T2 best-of-N KL bound · T3 flat-reward no-go · T4 plurality/Condorcet gate ·
T5 MBR SLLN consistency · T6 best-of-N `O(√log N)` regret. Each archive §3 cites the theorem that
backs its direction.

## Status legend

`planned` → `running` → `passed` (reproduced + red-team survived) / `scoped` (accepted with caveats) /
`refuted` (a blocking challenge stands; reworked or dropped).
