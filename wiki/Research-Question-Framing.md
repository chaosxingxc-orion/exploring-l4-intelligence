# Research-Question Framing — the focused question and its two branches

> **The north-star for the current phase (owner, 2026-07-04).** The whole program reduces to one
> focused question with a two-branch decision tree. Everything we build — the survey (theory leg), the
> CP directional checks (experiment leg), the validation table — exists to answer Q1 decisively and
> then take the correct branch. This doc is the decision spine; it is updated as evidence lands.

---

## Q1 — Is the optimization space of in-context learning for training-free RL in omni models sufficient?

**Scope.** Frozen omni speech model (no weight/structure change); the semantic layer (ASR/ST, SLU,
Spoken-QA/reasoning, Speech-Agentic); the lever is instruct-prompt / ICL conditioning + reward-guided
selection over the model's own rollouts.

**Operational definition (from the sufficiency yardstick, [[2026-07-04-sufficiency-yardstick-memo]]).**
"Sufficient" for a task family T means the **prompt-space contribution is non-trivial AND realizable**:

    H_prompt(T,K,N) − H_fix(T,N) ≥ δ_T   (reachability — the space instruct-prompting opens beyond one fixed instruction)
    ρ(T) ≥ ρ_min                          (realizability — a label-free selector actually harvests it)

with the genuine-accuracy split b2 (not b1 format artifact) required. **Program-level sufficiency** =
across the semantic layer, instruct-prompt rollout on the frozen omni reaches enough headroom,
reachably and genuinely, that training-free RL over the prompt/ICL space is worth building on.

---

## The two legs of evidence

### Theory leg (established by the reviewed survey [[2026-07-04-stage1-semantic-tfrl-survey]])
- The **magnitude of H_prompt − H_fix is unmeasured everywhere** for audio-in models — the central
  empty cell (text-domain APE/OPRO/GEPA quantified it; no audio analog; PromptingWhisper is a
  two-point existence-positive that bounds nothing).
- **Reachability (b) has NO theorem** — it is an empirical parameter per family; only (a) support
  (order statistics, KL ≤ log N − (N−1)/N bound) and (c) realization (N* over-optimization) have theory.
- Realization (c) is **documented-hard**: MBR null, the house ρ(ASR) ≈ 0 prior [hypothesis-grade].

### Experiment leg (the CP directional checks — small-n, worth-investment, Stage-1)
Each check measures H_prompt − H_fix and/or ρ on one surface; see [[Semantic-Task-Validation-Table]].
- ASR probe (n=50): **Δ_BM ≈ 0** (matched-budget), uninformative-to-weakly-fix-favoring.
- SLU intent, MInDS-14 (E1, n=150 **done**): **H_prompt − H_fix = +0.000** (CI [−0.02,+0.02]); greedy 0.953
  (near-saturated); b2-share over the random-label floor only +0.013 (CI [0.0,+0.033]); the fixed instruction
  wins best on 143/150. **Prompt-space ≈ nil on easy intent** — but the surface is near-ceiling, so this is
  as much 'ill-posed surface' as 'insufficient space'. *(directional)*
- Pending: SQA-MCQ (E3), selector anatomy ρ (E4), voice-agent (E5).

**Current lean (honest, not yet an anchor).** Both legs point the same way *so far*: the prompt-space
contribution looks **small / not-clearly-realizable** on the surfaces checked. But we have not yet
tested the harder / less-saturated surfaces (SQA reasoning, multilingual/OOD intent, agentic) where
prompt structure could matter more. **We do not anchor Q1 until enough surfaces are checked.**

---

## Decision criteria (what flips Q1)

| Verdict | Requires |
|---|---|
| **SUFFICIENT → branch 2.1** | Across ≥2 semantic families, H_prompt − H_fix shows a non-trivial (≥δ_T), **b2-genuine** (survives the format floor), **realizable** (ρ ≥ ρ_min) signal — directional first, then confirmed at Stage-2 n. |
| **INSUFFICIENT → branch 2.2** | H_prompt − H_fix ≈ 0 (or b1-only, or unrealizable) across the checked surfaces, with the theory leg (no (b)-theorem + measured nulls) corroborating. |

A surface being **near-saturated** (greedy already ≈ ceiling, as MInDS intent appears) is a third
outcome: it argues Q1 is *ill-posed on that surface* (no headroom for anyone), pushing the check to
harder surfaces before any anchor.

---

## Branch 2.1 — if the space IS sufficient

Then we discuss and build (methods to settle with the owner):
1. **Which training-free RL schemes are feasible** on the frozen omni: reward-guided best-of-N / MBR;
   prompt-search (OPRO/GEPA-shaped instruction optimization); ICL demo/exemplar selection;
   controlled/reward-guided decoding; self-consistency-with-verifiable-reward.
2. **How to define the multimodal optimization space** — the (q₀, conditioning family {q₀(c)},
   verifiable reward R) triple: what the reachable action space is when the input is audio + text +
   (optionally) image, and how conditioning moves q₀'s mass.
3. **Continuous improvement over the baseline** — whether the scheme compounds (iterated
   prompt-refinement, reward-model-free selection improving with N), and the specific method choice
   (to discuss).

## Branch 2.2 — if the space is NOT sufficient

Then, in order:
1. **Anchor the insufficiency conclusion rigorously** — theory (the survey's (b)-has-no-theorem +
   the support/realization bounds) + experiment (the CP nulls across surfaces, with grade discipline
   and, for the anchor, a Stage-2-powered confirmatory n on the decisive surface). This is a genuine,
   publishable negative result about the reachable prompt-space of frozen omni models.
2. **Then discuss omni agentic system feasibility as EXPLORATION-SPACE EXPANSION** — the agentic layer
   as a way to *enlarge the reachable action space* beyond what fixed-q₀ instruct-prompting reaches
   (new conditioning sources, tool-mediated support injection, decomposition that creates new
   verifiable sub-rewards), aiming for **further gains on experimental data**.
   - **Closure-fence note.** The 2026-07-03 NO-GO closed the specific question "build a *cross-session
     accumulating memory* agent NOW to add headroom on a *fixed* reward." Branch 2.2 is a *different*
     framing (expand the exploration/optimization space, possibly via new reward structure or support
     injection) — but any 2.2 mechanism that reduces to cross-session accumulation collides with the
     closure and needs an owner amendment (r1–r3). Crucially, **anchoring Q1-insufficiency with theory
     + experiment is itself the kind of new grounding** the closure contemplated: it converts "the
     single model's prompt-space is provably/measurably capped" from assumption into evidence — the
     precondition for a well-posed agentic-expansion argument.

---

## Where the current work sits

We are executing the **experiment leg of Q1** as small directional worth-investment checks (E1–E5),
theory leg already delivered by the survey. The immediate goal is to accumulate enough
surface-coverage to take Q1 to a defensible verdict at the next owner checkpoint — not to prejudge it.
The near-saturation of MInDS intent (E1) is itself a finding: it says *pick harder, less-saturated
surfaces* (SQA reasoning, multilingual/OOD, agentic) to give the prompt-space a fair chance before
anchoring insufficiency.

## 中文摘要

**聚焦问题 Q1:** 冻结 omni 模型上 ICL/training-free RL 的优化空间是否足够(语义层)?操作定义(充分性
标尺):prompt 空间贡献 H_prompt − H_fix ≥ δ 且可实现 ρ ≥ ρ_min,且是真精度 b2 非格式 b1。
**两条证据腿:** 理论(survey 已证 H_prompt 量级无人测、(b) 无定理、(c) 实现困难)+ 实验(CP 小样本
方向性检查:ASR 探针 Δ_BM≈0、SLU 意图 E1 早期 H_prompt−H_fix≈0 且近饱和)。目前两腿同向偏"prompt
空间小/难实现",但**尚未测更难的面(SQA 推理、多语/OOD、agentic),不锚定**。
**分支:** 2.1 若足够→讨论可行的 training-free RL 方案、多模态优化空间的定义(q₀/条件化/奖励三元组)、
能否基线持续提升(具体方法待议);2.2 若不够→先用**理论+实验锚定"不够"这个结论**(一个真实的负结果),
再讨论 omni agentic system 作为**扩展探索空间**的可行性以在实验数据上取得进一步收益。关闭围栏:7/03
的 NO-GO 关的是"固定奖励下建跨会话记忆 agent",2.2 是不同框架(扩展探索/优化空间);但**用理论+实验
锚定 Q1-不足本身就是关闭条款所设想的新依据**,把"单模型 prompt 空间受限"从假设变成证据。
