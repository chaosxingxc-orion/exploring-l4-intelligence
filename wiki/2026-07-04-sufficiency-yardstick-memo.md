# Sufficiency yardstick memo v0 — "is the instruct-prompt rollout optimization space sufficient?"

> Stage-1 framework document. Defines the operational yardstick the survey campaign's lanes are
> briefed against; v1 (post-synthesis) will fill the evidence tables with graded survey findings
> and a Stage-2 measurement-plan sketch. The question (owner, 2026-07-04): from the ICL
> perspective, is the optimization space of instruct-prompt-driven rollout on a frozen omni
> speech model sufficient for SEMANTIC tasks — and only if not, should an agentic system extend it?

## 1. Why a yardstick is needed first

The archives establish that "sufficiency" currently has no measurable definition: theory bounds
the *reachable distribution under selection on a fixed q₀* (KL ≤ log N − (N−1)/N; over-optimization
optimum N*), but **no support-expansion / ceiling-movement theorem exists** (verified negative
finding, 2026-07-03 delta scan), and "the space exists" has never been separated from "the space
is reachable by prompting." Answering the owner's question without first fixing definitions would
repeat the mechanism-first error.

## 2. The yardstick — a chain of fractions per task family T

Let m be the family metric, K an instruction/task-definition set size, N a sampling budget:

- **H_fix(T, N)** — oracle-over-sampling headroom under ONE fixed instruction.
  *(Condition (a), SUPPORT, restricted to the current setup. In-house scoped anchor: ASR
  +0.0418 [0.0289, 0.0564] @ N=8/SNR-5 — one instruction, one model, one condition.)*
- **H_prompt(T, K, N)** — oracle headroom when sampling ranges over K instructions × N rollouts.
  **H_prompt − H_fix is the prompt-space contribution** — zero in-house measurement, zero
  published quantification for omni speech models (verified). This difference is the campaign's
  intellectual center of gravity and the direct operationalization of the owner's question.
- **ρ(T)** — best label-free selector gain / H_prompt: the realization fraction.
  *(Condition (c), SELECTION-REALIZABILITY. House prior: ρ ≈ 0 for ASR — MBR null on two slices,
  memory selector exact zero [hypothesis-grade]; one external positive: frozen-LM MBR utility,
  9.0% rel WER, arXiv:2606.23306.)*

**Sufficiency(T) at budget (K, N)** := H_prompt(T, K, N) ≥ δ_T **and** ρ(T) ≥ ρ_min.
Stage 1 does NOT measure these to significance — it (i) bounds plausible ranges from others'
published numbers, (ii) fixes definitions so Stage 2 has a pre-registrable target, (iii) runs at
most one directional probe (pre-authorized: K instructions × small N on MInDS or LibriSpeech,
≤ half GPU-day, ≤ 200 items, single-touch, `directional-only`).

## 3. Condition (b) — reachability — carries the artifact split internally

A prompt-driven lift that is format normalization does not count as reachability of task mass
(ALICE: demos fix format, not accuracy). So (b) splits:
- **b1** — format/schema-compliance movement;
- **b2** — genuine accuracy movement, certified by label-sensitivity + acoustic-grounding
  controls (definitions reused from the 2026-06-26 proposal §2(iii); used here as *definitions*,
  not run gates).

Grading note: MInDS-14 +0.126 [0.077, 0.181] is evidence for (b) on the retrieval surface —
**b1/b2-unsplit** until an ablation separates them.

## 4. The theory asymmetry (stated plainly)

(a) and (c) have theory: order statistics of best-of-N, the KL trust-region bound, the
over-optimization ceiling N*. **(b) has no theorem.** The only honest theoretical statement about
prompt-reachability today: *unbounded above and below by current theory; an empirical parameter
per task family.* The nearest formal object — ICL-as-Bayesian-inference (arXiv:2510.10981) —
moves the task posterior but states no headroom result, and is proven in a meta-learning toy
setting. Consequence: (b) is where the survey's argumentation burden is heaviest, and where
cross-domain (text-LLM / VLM) evidence matters most: the text-LLM prompt-optimization literature
(APE / OPRO / GEPA class) is the only place prompt-space headroom has been quantified at all.

## 5. Failure routing — the problem generator

Each condition's failure opens a DIFFERENT research-problem family. This is how the agentic
question legitimately re-enters (as a conditional, never the starting point):

| Fails | Meaning | Problem family opened | Key survey evidence class |
|---|---|---|---|
| (a) SUPPORT | frozen q₀ lacks high-reward mass for T | external support injection (retrieval / hypothesis generation / lexicon) — the agentic re-entry point | ProGRes (5–25% rel WER via prompted generation of NEW hypotheses), RECOVER (8–46% entity correction), kNN-Whisper — all text-LLM-over-ASR or datastore; **"the omni expands its own support" is the unoccupied cell** |
| (b) REACHABILITY | mass exists but instruct/task-def/ICL cannot move q₀ onto it | conditioning research: task-activating prompting, ICL selection, iterative re-prompting; agentic re-prompting loops as escalation | TAP (arXiv:2309.15649), ALICE format-vs-accuracy, MiMo-Audio scale-emergence, APE/OPRO-class headroom distributions (text domain) |
| (c) REALIZABILITY | reachable but not pickable label-free | selector research (single-model, P-D-compatible) — the house-documented gap | self-certainty, CTC-oracle-gap anatomy, self-consistency/plurality (text-domain replicated) |

**Closure fence.** The NO-GO closed "cross-session accumulating agent" (re-open only on r1–r3).
Any candidate problem reducing to cross-session memory is flagged "collides with closed question —
owner amendment required," never silently ranked.

## 6. What survey evidence can establish, per condition × family (lane evidence contract)

| Condition | ASR/ST | SLU | Spoken-QA + reasoning | Speech-Agentic |
|---|---|---|---|---|
| (a) | n-best oracle-gap literature (30 yrs), MBR-ASR, GER/Hyporadise oracle tables → survey can settle magnitude | pass@k / candidate diversity on audio-LLMs — likely sparse; report absence explicitly | closed-form MCQ makes (a) near-trivial — define as calibrated non-degenerate mass | likely unmeasured → itself a named gap |
| (b) | prompted rescoring/generation (ProGRes, TAP) — text-LLM-over-ASR transfer caveat mandatory | TAP-style task-def results; in-house +0.126 (scoped, b1/b2-unsplit); ALICE | instruction/CoT-variant deltas in benchmark ablations | agentic-pipeline papers where the "agent" is prompt scaffolding |
| (c) | self-certainty; frozen-LM MBR utility (+); house nulls (−) | LLM-judge / consistency votes; trained rerankers fence-tagged OUT | self-consistency (well-replicated in text) | reward = verifiable task success (tau2-style envs) — (c) may be EASIEST here |

## 7. 中文摘要

充分性标尺 = 分数链而非布尔：**H_fix**（单固定指令 oracle headroom，ASR 已有 +0.0418 限定锚点）→
**H_prompt**（K 条指令 × N 采样的 headroom；**H_prompt − H_fix = prompt 空间贡献，in-house 与文献
双零测量，是本战役智力重心，也是 owner 问题的直接操作化**）→ **ρ**（无标签选择器实现分数，house
先验 ≈0）。充分性 = H_prompt ≥ δ 且 ρ ≥ ρ_min；Stage-1 只做定义固定 + 文献定界 + 一个定向探针。
(b) 可达性内部强拆 b1 格式伪影/b2 真实精度；理论不对称明示：(a)/(c) 有定理，**(b) 无定理**——
survey 论证负担最重、跨域（文本 LLM prompt 优化文献是唯一量化过 prompt 空间的地方）证据最关键。
失败路由即问题生成器：(a) 败→支撑注入（agentic 合法重入口，"omni 自身扩展自身支撑"是空格）；
(b) 败→条件化研究；(c) 败→选择器研究。关闭围栏：归约为跨会话记忆的候选一律标注碰撞、需 owner
修正案。
