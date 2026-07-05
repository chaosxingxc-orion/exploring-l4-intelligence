---
title: "Pre-registration (P1) — can adjusting A realize the confirmed oracle-δ? (Stage-1 directional)"
date: 2026-07-05
stage: 1-directional
status: FROZEN (committed before any P2/E-run; git timestamp is the anchor)
owner_pins: "relative +10% bar · zh+en only · SLU included · no model training · omni-reward = two context-differentiated systems"
---

# P1 — Frozen pre-registration for the A-realization program

> **Committed BEFORE any baseline or experiment run** (the strict review's "undefined thresholds →
> unfalsifiable" finding forced this). Stage-1 directional: small-n per set, broad coverage, grade every
> number `[directional | small-n | not significance-bearing]`; per CLAUDE.md this **settles nothing**
> statistically — it is a logical-self-consistency signal for the owner's branch discussion.

## 1. The frozen question
Can adjusting the conditioning **A** (multimodal few-shot ICL; global prompt optimization; a
context-differentiated omni verifier) convert the confirmed per-instance **oracle-δ** (best-of-N headroom)
into a **deployable greedy/default-output gain** — i.e. shift P(X|A) so the good answer becomes modal /
label-free-selectable — and does it **transfer** to held-out? → branch 2.1 (space is TFRL-optimizable) vs
2.2 (need agentic reward/verification expansion).

## 2. Coverage set (frozen, zh+en, on-disk, non-saturated — 9 datasets, 4 families)
| Family | English | Chinese |
|---|---|---|
| SQA / audio-reasoning MCQ | mmau-mini, big-bench-audio, vocalbench | vocalbench-zh, uro-bench/OpenbookQA-zh |
| ASR (WER) | librispeech | — |
| Extractive QA (EM/F1) | spoken-squad | uro-bench/SQuAD-zh |
| SLU (intent+slot) | slurp | minds14/zh-CN |

Any set whose greedy baseline is ≥ 0.90 (near-saturated) is demoted to an easy-anchor and excluded from
the coverage-verdict (P2 confirms saturation per set). n per set: **150–300** (Stage-1).

## 3. Success criteria (frozen NUMBERS)
- **δ_T (self-consistency bar):** a lever "works" on a surface iff its deployable gain is **relative
  ≥ +10%** over the fixed-A greedy baseline (e.g. 0.60 → ≥ 0.66), paired-bootstrap CI excluding 0.
- **Coverage requirement:** the lever must clear δ_T on a **majority of the non-saturated coverage set**
  (≥ ⌈N_nonsat/2⌉ surfaces, both languages represented) — breadth, not one surface.
- **b2-genuine (not format):** the gain must survive a **random-label / shuffled-exemplar floor** (b1) —
  report gain over the b1 floor, CI excluding 0.
- **Transfer:** for E8 (global prompt-opt), the held-out/dev retained ratio ≥ **0.7**.
- **ρ / realized-δ fraction:** report (greedy(A_best) − greedy_fix)/oracle-δ per surface.

## 4. Levers & controls (frozen)
- **E7** multimodal few-shot ICL: shot-curve k∈{0,1,2,4,…max}; b1/b2 control; leakage guard (exemplars
  from train only, never the test item).
- **E8** global prompt optimization (OPRO/GEPA-style, dev-label-scored, in-fence; no per-utterance
  selector on MCQ); measure transfer.
- **E10** omni verifier = **two context-differentiated systems** (generator-agent / verifier-agent, same
  frozen weights, distinct system-prompt); measure error-decorrelation δ_corr vs E4 coupled self-judge;
  **no model training**; the shared knowledge-blind-spot floor is PARKED (#37 → W4 omni-embedding).
- **CMP** A-shift vs selection at **matched budget**.

## 5. Statistics (frozen)
Paired percentile bootstrap over utterances, 10,000 replicates, seed-fixed; "n.s." = 95% CI crosses 0.
Every reported number → a committed `_repro/*.json` with a `reproduce:` line. Greedy is **temp-0
nondeterministic** under llama.cpp MoE — report it as a single estimate, disclose the backend.

## 6. Decision rule (frozen, applied mechanically at DEC/#35)
- **→ 2.1** iff ANY in-fence lever (E7/E8/E9 A-adjustment, or E10 verifier) clears δ_T (relative +10%),
  b2-genuine, transfers (E8), across the majority-coverage requirement, both languages.
- **→ 2.2** iff all in-fence levers fail the above — then an agentic reward/verification expansion is
  warranted (gain_product-respecting: a non-isolated τ-reducing verifier or a genuinely new
  independent-of-M verifiable reward), carrying a C1–C4 convergence proof, behind the 2026-07-03 closure.
- Either way: number ledger + 4-persona strict re-review ACCEPT before lock; **returned to owner, no
  automatic rollover to Stage-2.**

## 中文摘要
冻结判据(跑前提交):问题=调 A 能否把 oracle-δ 变可部署 greedy 增益且 transfer。覆盖=9 个中英集(4 族,含
SLU),每集 150–300,近饱和(greedy≥0.90)剔除。阈=**相对 +10%**(配对 bootstrap CI 不跨零),须**过半覆盖面**
且中英都有、b2 真(过随机标签地板)、E8 transfer≥0.7。杠杆=E7 多模态 few-shot / E8 全局 prompt 优化 / E10
两系统(generator-verifier,不训练)。判定:任一 in-fence 杠杆达标→2.1;全败→2.2(独立于 M 的新奖励/验证 +
C1–C4 收敛,守关闭围栏)。数字总账 + 严格复评 ACCEPT 才 lock,交主人。
