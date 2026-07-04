---
title: "Is in-context learning sufficient for training-free RL on frozen omni speech models? A Stage-1 directional finding (theory + experiment + Lean)"
date: 2026-07-04
revised: 2026-07-05 (v2 — after 4-persona strict review; see [[2026-07-05-Q1-conclusion-review-synthesis]])
stage: 1-conclusion
status: DIRECTIONAL (Stage-1); returned to owner for discussion — NOT a locked verdict, NOT a program decision
question: "Q1 — is ICL sufficient for training-free RL for omni models; if not, should we design an omni agentic system?"
scope_warning: "n=150, single model (Qwen3-Omni-30B Q8_0 GGUF, audio path EXPERIMENTAL), single operating point (temp 0.7, N=8), effectively ONE non-saturated surface (MMAU-mini MCQ). Small-n Stage-1 evidence 'can settle nothing' (CLAUDE.md) — hypothesis-grade until re-established at Stage-2."
---

# Q1 (Stage-1 directional) — is ICL sufficient for training-free RL on frozen omni speech models?

> **This is a v2 rewrite after strict 4-persona review** ([[2026-07-05-Q1-conclusion-review-synthesis]],
> decision: MAJOR REVISION). The v1 verdict ("ICL insufficient → build an agentic system", VERDICT-LOCKED)
> over-reached its evidence on three counts the panel caught and this version corrects: (i) it conflated
> "current weak instruments don't harvest" with "the space is insufficient"; (ii) its one affirmative
> result (multimodal +0.06) was a speed-driven artifact of an inadequate audit; (iii) it locked a
> program decision on Stage-1 n=150 evidence. **What survives is narrower, and honest.**

> **Method.** Theory leg (the reviewed survey + machine-checked Lean bounds) ⊕ experiment leg (small
> directional checks decomposed by the sufficiency yardstick). Every in-house number is grade-tagged and
> traces to a committed `_repro/*.json`. The conclusion is argued from literature + theory + the
> decomposed experiments, **held to what the instruments actually tested.** Framing:
> [[Research-Question-Framing]]; yardstick: [[2026-07-04-sufficiency-yardstick-memo]]; theory:
> [[Theory-Convergence-and-Constraints]].

## 1. The question, made precise

Q1 asks whether the **instruct-prompt / ICL optimization space** (conditioning c = text ⊕ multimodal) of
a frozen omni is *sufficient* for training-free RL on the semantic layer. The yardstick decomposes it:
- **(a) SUPPORT** `H_fix` — does the frozen model's sampling distribution hold high-reward outputs at all?
- **(b) REACHABILITY** `H_prompt − H_fix` — does conditioning (text ⊕ multimodal) move mass onto them
  beyond fixed-instruction sampling? (split b1 format / b2 genuine)
- **(c) REALIZABILITY** `ρ` — can a *label-free* selector actually harvest the headroom at deployment?

ICL-sufficiency = (b) is a real, genuine, realizable lever. **Caveat that governs the whole reading:**
each condition was probed with the *cheapest available instrument*, so a null is evidence about *that
instrument*, not necessarily about the *space*.

## 2. The evidence, by condition — held to what was tested

### (a) SUPPORT — REAL where the task is non-trivial (one measurement, not two)
- MMAU-mini MCQ (E3/E4, n=150, same seed-frozen slice): greedy ≈ 0.633–0.640 → **oracle-over-8 = 0.773**;
  **H_fix ≈ +0.133–0.140** `[directional]`. *(E3 and E4 are the SAME oracle 116/150 over the SAME slice;
  the greedy base is temp-0 **nondeterministic** under the llama.cpp MoE backend — E3 96/150 vs E4 95/150 —
  so this is one ~+0.133–0.140 estimate, not two independent corroborations.)*
- ASR (C1): oracle best-of-N headroom +0.0418 [0.029, 0.056] `[scoped]`.
→ The frozen omni's sampling distribution genuinely contains much better outputs than greedy — sampling
  rollout is the real value carrier. (This is oracle/label-aware headroom; deployability is condition (c).)

### (b) REACHABILITY — the tested levers are inert, but the STRONGEST levers were not run
- **Text, UN-OPTIMIZED instruction diversity.** SLU intent MInDS-14 (E1, n=150): H_prompt−H_fix = **+0.000**
  (near-saturated surface, greedy 0.953). SQA-MCQ MMAU (E3, n=150): **+0.020** (CI [−0.02,+0.06], n.s.;
  b2 vs generic +0.027, n.s.). These use K≈8 **hand-authored** instructions. **This establishes that naive
  instruction variation is inert — NOT that the prompt space is barren:** the OPRO/GEPA-style
  reward-scored *optimized* prompt search (the actual training-free-RL-over-prompt method, and the
  survey's flagged "central empty cell") was **not run.** On MMAU MCQ an offline dev-label-scored prompt
  search is in-fence and needs no per-utterance label-free selector at all.
- **Multimodal, acoustic presentation (E6′, M1 only).** The FBank-invariance audit correctly excluded
  content-altering transforms (rms_norm 0.978, preemphasis 0.886, denoise 0.926 — which hurt to 0.587,
  telephone 0.931). But the headline **H_mm = +0.060 does not survive scrutiny:** recomputed from the
  artifact, **100% of it is driven by the two speed transforms** — oracle{original, trim} = 0.640 =
  greedy → **H = +0.000**, and trim adds nothing to the speed pair. The gate compares **time-averaged**
  log-mel, which is length-robust *by construction*, so a ±10% time-stretch scores 0.993 and passes while
  changing duration/tempo/counts — exactly the leakage MMAU's temporal/counting items are vulnerable to.
  **So E6′ does not establish a valid multimodal conditioning gain.** The two stronger multimodal
  sub-channels — **M2** audio few-shot ICL and **M3** leakage-audited cross-modal (transcript/lattice)
  injection, where the survey's own evidence is strongest ([134][112][136]) — were **not tested.**
→ On the tested levers, reachability ≈ 0; but the decisive levers (optimized prompt search; M3 cross-modal
  injection) are **untested**, so "(b) is barren" is **not** established.

### (c) REALIZABILITY — cheap self-referential selectors under-harvest; the class that works was not tested
- MMAU (E3): majority = greedy exactly.
- MMAU (E4, n=150): greedy 0.633, oracle 0.773 (headroom +0.140). Cheap **self-referential** selectors:
  self-certainty **ρ = 0.0**, majority/conf-weighted-vote **ρ = −0.047**, **LLM-judge (same model judging
  itself) ρ = 0.143** — a directional **positive** (~14% of headroom, ~+2 acc pts) whose CI vs majority
  [−0.013, +0.067] merely fails to exclude 0 at n=150 (**under-powered, not a confirmed zero**).
- **Not tested:** the in-fence selector class the survey says is the *only* one to yield an in-fence
  positive — an off-the-shelf **trained utility / reward model used as-is**, or a **frozen-LM
  pseudo-log-likelihood MBR** utility ([25], ~9% rel WER on ASR). C4's τ is **selector-specific**: τ for a
  trained verifier can be far below τ for a self-judge.
→ **Cheap, self-referential selection does not harvest the real oracle headroom on this surface.** Whether
  a trained-verifier selector does is the open, untested question — and it is exactly the (c) lever.

## 3. Theory anchor (Lean, machine-checked) — stated at the strength the Lean actually proves

- **(a) support** — `OptSpace`: reward-guided tilting `q* ∝ q0·exp(R/β)` is the KL-constrained optimum
  (`Tilting.tilting_optimal`; β = C1 trust-region term). Gain is `≥0` (`gain_nonneg`), **strictly positive
  iff the reward is non-degenerate** (`gain_pos_of_nonconstant`), zero under a flat reward (`flat_no_gain`).
  The quantitative `spread²/(8β)` cap (`gain_le_of_hoeffding`) is **hypothesis-gated** — it *assumes* the
  Hoeffding estimate `S` and returns `gain ≤ S`; the machine-checked content is only the reduction
  `gain = β·log Zpart − E[R]`. (Disclosed here symmetrically with the Beirami `sorry` below — Hoeffding's
  lemma itself is not formalized.)
- **(c) realization** — `Realization` (sorry-free): for a finite pool, a selector picking `argmax Rhat`
  vs any reference `jstar` satisfies `R(jstar) − R(selector) ≤ 2·τ`, `τ` any uniform bound on `|Rhat − R|`
  (`realized_gap_le_two_tau`; needs only that `jhat` maximizes `Rhat`); `τ=0 ⇒ ρ=1`
  (`exact_estimator_is_oracle`); and **as a convergence statement**, along any selector sequence with
  `τ_n → 0` the realized reward → oracle (`realized_tendsto_oracle`, squeeze — one-directional; the
  converse is not claimed). **This is a conditional bound: it explains WHY a high-τ selector fails; it does
  NOT prove τ is large for every selector.** So it is consistent with E4 (self-judge high τ, ρ≈0) *and*
  with a trained verifier having small τ.
- **Agentic-composition boundary** — `OptSpace.gain_product` / `qstar_product`: for a **context-isolated**
  product action space with an **independent** base and a **separable/additive** reward, the gain is
  additive and the isolated optimum equals the monolithic optimum. **Strictly:** *context-isolated,
  separable-reward composition* buys no headroom — extra gain needs either a genuinely new non-degenerate
  reward **or reward non-separability/interaction**. It does **NOT** cover a non-isolated composition (a
  critic / reranker / verifier that re-examines the *same* output space to lower τ) — which is exactly the
  (c)-lever below. So the theorem forecloses only naive duplicate-agent stacking, not agentic verification.
- **Honest asymmetry.** (a) and (c) have theorems; **(b) has none** — there is no support-*expansion*
  theorem for prompting (tilting reweights the existing support; the library has no object for "different
  prompt → different base/support"). The measured text-null is consistent with this gap, not a proven
  impossibility.

`[Lean status: VERIFIED. Full TfrlProofs builds against Mathlib v4.31.0 (toolchain + mathlib both pinned
v4.31.0); all cited theorems sorry-free. The ONLY library sorry is the documented Beirami order-statistics
derivation (BestOfN.klBoN_le_klBoundBoN_TODO), unused by this conclusion. The `spread²/(8β)` figure is
hypothesis-gated (see above), disclosed symmetrically.]`

## 4. The verdict (Stage-1 directional — for owner discussion)

**Q1 answer, held to the evidence: the ICL levers we tested do not help — but "the ICL optimization space
is insufficient" is NOT established, because the decisive stronger instruments were not run.** Precisely:

1. **Un-optimized instruction diversity is inert** on both an easy (E1) and a hard (E3) surface — the naive
   text-prompt lever is not it. *(The optimized OPRO/GEPA-style prompt search is untested.)*
2. **Cheap self-referential label-free selection does not harvest** the real oracle headroom (E4). *(A
   trained-verifier / MBR selector — the class known to work in-fence — is untested; the best self-selector
   already trends positive but under-powered.)*
3. **The one affirmative signal (multimodal +0.06) is a speed-driven artifact** of an inadequate
   time-averaged audit; under genuinely-safe transforms it is +0.000. *(M2/M3 multimodal channels untested.)*
4. **Real latent oracle headroom exists** (sampling +0.13) — so the frozen model is not the bottleneck;
   **the open problem is (c) realization.**

So the honest Stage-1 finding is **not** a program-level "insufficient." It is: *on one MMAU MCQ surface of
one quantized omni, at one operating point, the cheap/naive ICL instruments fail to convert a real oracle
headroom into deployable gain; the realization gap is the live problem, and the stronger in-fence
instruments that could close it — optimized prompt search, a trained-verifier selector, M3 cross-modal
injection — were not run.* Per the Stage-1 rule this **settles nothing**; it is returned to the owner to
decide the next probe, not rolled into a branch.

## 5. Does this point to an omni agentic system? — open, and NOT forced by the theory

**No theorem forces it, and the evidence does not yet choose between the two branches.** Both are live:

- **Branch 2.1 (space is workable, realization is the lever).** The cleanest reading of "large oracle
  headroom + weak harvest" is that the *selector* is the deficient component — pointing to a **stronger
  in-fence selector** (trained utility / frozen-LM MBR / better-calibrated confidence) and/or an
  **optimized in-fence prompt search** (OPRO/GEPA with dev labels — no per-utterance label-free selector
  needed). These are the untested instruments from §2 and should be run **before** any agentic build.
- **Branch 2.2 (exploration/reward expansion).** If those in-fence levers also fail, an omni agentic system
  is warranted *specifically* to lower τ via **tool-mediated verification** (turn a label-free guess into a
  *verifiable* signal) or to add a **genuinely new verifiable reward / cross-modal grounding**. Note
  `gain_product` does **not** license this — it only forbids naive isolated agent-stacking; a τ-reducing
  verifier is a **non-isolated** composition the theorem is silent on. So the agentic case is
  *motivated-but-not-theorem-forced*, and any such design still ships a C1–C4 convergence proof and stays
  behind the 2026-07-03 closure fence (no reduction to cross-session-memory-on-fixed-reward without r1–r3).

**One-line answer.** On the surfaces and instruments tested, the *cheap/naive* ICL levers are insufficient
to realize the frozen omni's real latent headroom — but whether the *optimization space* is insufficient is
**undecided**, because the strongest in-fence levers (optimized prompt search, trained-verifier selection,
M3 cross-modal injection) were not run. The disciplined next step is to run those in-fence instruments on
≥2 non-saturated surfaces; only if they also fail does the omni-agentic (reward/verification-expansion) case
become the anchored recommendation. This is a Stage-1 directional signal for the owner, not a decision.

## 中文摘要（v2，经四人严格评审后修订）

**Q1（Stage-1 方向性，交主人裁决——非锁定、非分支决策）:** 冻结 omni 语义层上,**我们测的 ICL 杠杆
无效,但"优化空间不足"未被证明**,因为最有力的 in-fence 工具没跑。
1. **未优化的指令多样性惰性**(E1 +0.000、E3 +0.020 n.s.)——朴素文字 prompt 不是杠杆;**但 OPRO/GEPA 式
   奖励打分的优化 prompt 搜索(真正的 training-free-RL-over-prompt 方法、survey 的"中心空白格")未跑。**
2. **廉价自指选择器未能实现** oracle headroom(E4:自判 ρ=0.143 是欠功效的**正向**、非确证零);**已知唯一
   in-fence 有效的选择器类——现成训练好的 verifier/reward model 或冻结-LM MBR([25])——未测。** C4 的 τ
   是选择器特定的:训练 verifier 的 τ 可远小于自判。
3. **唯一的正向信号(多模态 +0.06)是 speed 变换伪影**:重算 oracle{original,trim}=0.640=greedy → **+0.000**;
   时间平均的 mel 门天然对时长鲁棒,±10% 变速得 0.993 通过门却改了时长/节拍/计数——正是 MMAU 时序题的泄漏。
   **E6′ 未确立合法多模态条件增益;M2/M3(尤其跨模态注入)未测。**
4. **真实 oracle headroom 存在**(采样 +0.13)——冻结模型非瓶颈,**开放问题是 (c) 实现。**
诚实的 Stage-1 结论:**在一个 MMAU MCQ 面、一个量化 omni、一个工作点上,廉价/朴素 ICL 工具未能把真实
oracle headroom 转成可部署增益;实现差距是活问题,能补的更强 in-fence 工具没跑。** 按 Stage-1 规则**settle
不了任何东西**,交主人定下一步。

**是否 omni agentic system:开放,理论不强制。** 两分支都活:**2.1** 空间可用、实现是杠杆 → 先跑更强
in-fence 选择器 + 优化 prompt 搜索;**2.2** 若这些也失败 → agentic 专用于降 τ(工具验证把无标签猜测变可验证
信号)或加新可验证奖励/跨模态 grounding。`gain_product` **不**授权此建议——它只禁朴素隔离堆 agent,降 τ 的
verifier 是**非隔离**组合、定理未涉;故 agentic 是**有动机非定理强制**,仍需 C1–C4 收敛证明、守 7/03 关闭围栏。
