# Stage-1 reflection — re-grading the evidence base under the three-stage methodology

> Dated reflection doc per the Research-methodology section of CLAUDE.md (records are append-only;
> this doc layers grades on top of prior records and rewrites nothing). Trigger: the owner's
> 2026-07-04 methodology calibration — we are in **Stage 1 (problem definition)**, where
> argumentation must stand on literature + theory, and in-house small-n numbers are directional
> signals only.

## 1. What the calibration correctly identifies about our prior work

**1.1 Experiments were over-weighted.** The agentic GO/NO-GO campaign (Decision-Log 2026-07-04)
rested its two mechanical kills on Stage-1-grade samples: M3 = 36 utterances / 13 entities /
9 chapters / one corpus domain (audiobook read speech) / one model / clean-only; M5 = 144
utterances / 12 speakers / one noise condition. Procedurally airtight (pre-registered thresholds,
freeze-before-run commits); epistemically, reading them as *mechanism-class* verdicts exceeds what
small-n carries. The campaign's own review machinery partially caught this — the /ars-reviewer
panel forced the M5 relabeling to "inconclusive-by-inert-instrument → frozen default, **not**
empirical falsification of the mechanism class" — but M3's kill, though 38× over threshold, also
generalizes over exactly one domain.

**1.2 The deeper defect: no problem was ever pinned.** The arc from 2026-06-22 onward was
thesis-driven (activate pretrained knowledge) → operator-driven (A/B) → mechanism-driven (M1–M5)
— never **problem-driven**. At no point did we state: *recognized open problem P in
ASR/SLU/SQA/Speech-Agentic; existing approach X fails at Y; our method addresses Y.* The frozen
H1/H2/H3 (2026-06-26 proposal) are likewise mechanism-first. This is the root of the
"theoretical justification lacks soundness" critique: the argumentation hung on self-posed
mechanisms rather than literature-established problems.

**1.3 A concrete exposed hole.** The C1 best-of-N pipeline used **one fixed instruction**
end-to-end. The instruct-prompt optimization space on semantic tasks has **never been explored
in-house** — while our strongest surviving positive number (MInDS-14 +0.126, below) is precisely
a prompt/schema-surface optimization gain. We killed memory/support mechanisms without ever
measuring the more basic lever the owner now asks about.

## 2. Evidence re-grade

Grades: **settled** (multi-source, survives Stage-1 scrutiny) · **scoped** (real but
class/condition-limited) · **hypothesis-grade** (directionally consistent, not established) ·
**directional** (single small-n signal).

| Evidence | Prior use | Re-grade | Notes |
|---|---|---|---|
| Speaker never written to pooled vector (≤0.067, 37 layers × methods × seeds) | conclusion | **settled (vector class)** | multi-source: probes + 77-agent survey; generative class = lit-only, negative-leaning |
| Emotion present-but-unread; weight-free ceiling ~0.40–0.51 | conclusion | **settled (vector class), scoped** | readout problem, not destruction; +0.097 headline was corrected to NULL across seeds |
| Content/semantic axis high-fidelity (probe ≈1.0) | conclusion | **settled (vector class)** | the 2026-06-23 semantic pivot already recognized this |
| MInDS-14 intent +0.126 [0.077, 0.181] paired-CI | "Operator-B best-of-N gain" | **scoped** | survived forensic re-run; relabeled: frozen bi-encoder cosine selection over prompt/schema surface; b1(format)/b2(accuracy) split not yet done |
| C1 ASR oracle headroom +0.0418 [0.0289, 0.0564] | conclusion | **scoped** | real, but one model / one condition (SNR-5 chosen because it creates spread) / one fixed instruction — i.e. it measures H_fix, not H_prompt |
| MBR null at every N (two slices) | "deployable selectors are hard" | **hypothesis-grade** | consistent direction, 2 slices / 1 model / 1 noise condition |
| Anti-consensus headroom structure (91.8% rows / 93.8% mass) | supporting fact | **hypothesis-grade** | reproducible census, single 144-utt sample |
| M3 kill (F=0.381 vs 0.01) | mechanism kill | **directional** | strong signal that support condition (a) holds for clean read-speech lexical entities; NOT a general support theorem; 3/13 entities genuinely unsupported; ~75.6% of residual headroom on zero-support tokens (memo-grade census, committed) |
| M5 exact zero | mechanism kill | **directional / inconclusive** | inert instrument (median flip-λ 60.5 vs frozen 0.05); per the corrected decision doc: closes by frozen default, not falsification |
| r1/r2 negative existentials (no cross-session corpus; no non-separable bound) | conclusion | **settled (as of 2026-07-03)** | survey-grade, 12+ verified-empty searches; time-bounded |
| H1/H2/H3 (frozen 2026-06-26, never run) | pre-registered hypotheses | **inputs under re-grade** | mechanism-first; proposal marked superseded-pending-Stage-1; may be rewritten problem-first after the survey; resurrection by back-fitting is forbidden |
| SLURP +0.330 / URO +0.335 / URO rerank +0.130 | cross-team gains | **withdrawn** | forensics: no artifact / relabeled / remote-API tainted (deep-review provenance pilot) |

**Standing procedural note.** The NO-GO closure (question: "build a cross-session accumulating
agentic system now") remains procedurally valid for the question it closed — nothing here reopens
it. What changes is citation discipline: its experimental legs are cited at their re-graded level
above, per the methodology's "evidence keeps the grade of the stage that produced it."

## 3. Why the owner's reframed question is the right Stage-1 question

"From the ICL perspective, is the instruct-prompt rollout optimization space sufficient (semantic
layer)?" is better-posed than the killed agentic question because it is (i) **problem-first** —
anchorable to recognized open problems per task family; (ii) **survey-answerable** — what others
achieved with prompt/ICL optimization on speech-LLM semantic tasks is literature; (iii) equipped
with a cheap, Stage-1-appropriate directional probe (H_prompt − H_fix, see the sufficiency
yardstick memo); and (iv) it makes the agentic question a *conditional extension* (only if support
or reachability fails), consistent with the closure record.

## 4. 中文摘要

Owner 的方法论校准指出两点要害：① 小样本实验被当作决定性依据使用（M3/M5 的"机械化击杀"是
Stage-1 级的方向信号，不是机制类的死刑）；② 更深的病根是**从未钉死要解决哪个具体研究问题**
——弧线一直是主旨→算子→机制驱动，从来不是问题驱动。具体暴露的空洞：C1 管线全程一条固定
instruction，owner 所问的 prompt 优化空间 in-house 零测量，而幸存的最强正数字（MInDS +0.126）
恰是 prompt/schema 表面优化收益。证据分级表见 §2：向量类副语言结论**已定论**（speaker 从未写入
/emotion 存在但读不出）；MInDS 与 C1 headroom **限定有效**；选择器难度与反共识结构**降为假设级**；
M3/M5 **降为方向级**；SLURP/URO 数字**撤回**；H1-H3 标注 superseded-pending-Stage-1。
NO-GO 关闭程序有效不翻案，仅改变引用纪律。
