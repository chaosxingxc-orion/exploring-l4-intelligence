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

with the genuine-accuracy split b2 (not b1 format artifact) required.

**The conditioning space is text ⊕ multimodal (owner, 2026-07-04).** For an OMNI model the "prompt" /
conditioning c is *not only the text instruction* — it includes **multimodal signal injection and
adjustment**: acoustic conditioning (denoise / normalize / speed / filter / emphasis / segmentation),
cross-modal injection (transcript or a text view alongside the audio), audio few-shot exemplars, and
(where relevant) visual context. The diagnostic is **prompt → rollout sensitivity**: hold the task, vary
c, and measure how the rollout distribution (and its oracle headroom) moves. **E1/E3 measured only the
TEXT sub-channel of c** — they found the text-conditioning contribution ≈ 0. Whether the *multimodal*
conditioning channel moves the rollout is the omni-specific, still-untested part of Q1, and is the
priority next check. So H_prompt below is understood over the **full** c = {text} × {multimodal}.

**Integrity constraint on multimodal conditioning — judged at the FEATURE level (owner correction,
2026-07-04).** The semantic representation of audio does **not** live in the raw waveform; it lives in
the **high-order features (log-mel / FBank / MFCC)** that the model's audio encoder (Qwen3-Omni's
Whisper-style log-mel front end) actually consumes. So leakage/equivalence must be judged **at the
feature level, not the signal level** — my earlier blanket claim that "any acoustic transform changes
the answer-relevant evidence" was wrong at the wrong level of analysis. The corrected criterion:

> A waveform transform is a **valid, semantically-equivalent** conditioning (so `oracle-over-K` over
> it is legitimate, exactly as for text-instruction rewording) **iff it preserves the task-relevant
> FBank/MFCC content** — neither removing features the answer depends on nor adding features that
> encode the answer. This is **measurable**: compare the log-mel/MFCC of original vs transformed and
> require the task-relevant structure to be preserved (e.g. high mel-band cosine similarity), and it
> is **task-aware** (a denoise is feature-preserving for "what was said" but feature-destroying for
> "what is the background sound").

Consequences: **loudness normalization is feature-invariant** (a log-domain offset — the mel *shape*,
which carries the semantics, is preserved) → safe and oracle-legitimate. **Band-pass / aggressive
denoise remove mel bins** → feature-altering → invalid *for tasks that depend on that content*. **Small
pitch-preserving speed** mostly preserves mel structure for content questions but changes it for
counting/duration. So the design rule is: **run a per-transform FBank/MFCC-invariance audit, keep only
the transforms that provably preserve the task-relevant features, report the audit alongside the
result.** The universally-clean levers remain: **(M1)** feature-invariant transforms (loudness-class,
audited); **(M2)** non-leaking audio few-shot ICL (exemplars from *other* items — the test answer is
never in context); **(M3)** leakage-audited cross-modal injection. Every multimodal design ships its
feature-level leakage audit before it runs.

**Program-level sufficiency** =
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
- SQA-MCQ, MMAU-mini (E3, n=150 **done**): greedy 0.640 (non-saturated). **The decisive split:**
  **H_fix = +0.133** (condition (a) support is REAL and large — sampling reveals much better answers);
  **H_prompt − H_fix = +0.020** (CI [−0.02,+0.06], n.s.; b2 vs generic +0.027, n.s.) — condition (b)
  prompt-reachability ≈ 0 *even where headroom exists*; and **majority = greedy = 0.640** — condition
  (c) realization ≈ 0 (the deployable selector harvests 0% of the +0.133 headroom). *(directional)*
- SQA-MCQ realization, MMAU-mini (E4, n=150 **done**, same slice as E3): greedy 0.633, **oracle 0.773
  (headroom +0.140)**; the modern label-free selectors **all fail to harvest it** — self-certainty
  (mean-token-logprob) **ρ = 0.0**, majority **ρ = −0.047**, confidence-weighted vote **ρ = −0.047**
  (both *below* greedy), LLM-judge **ρ = 0.143 but n.s.** (CI vs majority [−0.013, +0.067] crosses 0).
  **No label-free selector significantly beats majority** — the "confidently-wrong" mechanism (C4:
  large reward-estimation error τ). **(c) realization ≈ 0 confirmed on modern selectors, not just
  majority.** `_repro/cp3_selector_realization_mmau.json`. *(directional)*
- Pending: multimodal-conditioning (b) leg (E6′, feature-audited — running), voice-agent (E5).

**Current lean (honest, sharpening — not yet a formal anchor).** Across BOTH an easy surface (E1
intent, near-saturated) and a hard, non-saturated surface (E3 MMAU, greedy 0.64) the picture is
consistent and now *decomposed by condition*:
- **(a) support is REAL** where the task is non-trivial: E3 H_fix = +0.133 (the frozen q₀ holds much
  better answers than greedy; sampling reveals them). So best-of-N / sampling-based training-free RL
  has genuine room.
- **(b) the instruct-prompt / ICL contribution ≈ 0** on both surfaces (H_prompt − H_fix ≈ 0, not
  b2-genuine). Instruction diversity is **not** the lever — this is the specific thing Q1 asks about,
  and the directional answer is leaning **insufficient**.
- **(c) label-free realization ≈ 0** — now tested across selectors, not just majority: E3 majority =
  greedy exactly; E4 (n=150) self-certainty ρ=0.0, majority/conf-vote ρ=−0.047, **best (LLM-judge)
  ρ=0.143 but not significant**. No deployable label-free selector harvests the +0.14 oracle headroom.
The nuance that matters for the branch: the value that exists lives in **sampling-support (a)**, which
neither **prompting (b)** nor **deployable selection (c)** currently captures. So the honest reframing
is: the *instruct-prompt optimization space* looks insufficient (→ 2.2 territory), but the *sampling
support* is real and the open lever is **(c) realization** — which E4 now shows current label-free
selectors do NOT close (the confidently-wrong / large-τ mechanism, machine-checked as C4 in
`TfrlProofs.Realization`). Remaining before a formal anchor: the multimodal (b) leg (E6′) and broader
surfaces; but the (a)/(b)/(c) decomposition — support real, prompt ≈ 0, realization ≈ 0 — is the finding.

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
