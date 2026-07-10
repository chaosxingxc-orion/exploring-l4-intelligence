---
title: "Cross-domain transfer reference: VLM / GUI / computer-use agents (2025-2026)"
date: 2026-07-06
stage: 1-argumentation
lane: xdomain-vlm-gui
---

> **🗄 ARCHIVED (2026-07-11)** — 已收官战役过程件（2026-07-06 omni-agentic 调研），仅作历史，非现行真源。

# Cross-domain transfer reference: VLM / GUI / computer-use agents

> Stage-1 lane, reference-only. Scope: VLM/GUI/computer-use agent methodology (memory, planning,
> tool-use, verification) 2025-01..2026-07, tagged `origin: VLM`, `transfer: untransferred` unless a
> speech instantiation is explicitly named. Every method gets two extra columns per the lane brief:
> **transfer candidate to speech** and **VLM-known-failure-when-transferred**. Delta-tagged against
> the archive (S1 agent-level-synthesis, S2 agent-memory-skills-design, L4 speech-agentic, X3
> LLM/VLM test-time map). All URLs fetched/searched and confirmed resolving 2026-07-06.
>
> **Relationship to X3** (`2026-07-04-stage1-X3-llm-vlm-testtime-map.md`): X3 covers general
> LLM/VLM *test-time methodology* (ICL, CoT, self-correction, prompt optimization) at the
> single-turn-reasoning level. This lane is narrower and complementary: it covers GUI/computer-use
> **agent-architecture** patterns — persistent skill/knowledge memory, multi-agent role
> orchestration, and verification-as-tool vs verification-as-role — none of which X3 or the S1/S2
> agent-memory archive (Mem0/AriGraph/Zep-class, text/embodied-robot-origin) already cite. All 13
> claims below are new sources not previously recorded in the wiki.

## Summary verdict (test, not assume, the organizing framework)

Reading the 2025-2026 GUI/computer-use literature through the element/usage-pattern/constraint lens
gives a consistent pattern: **wherever a GUI-agent framework crosses a capability boundary, the
literature itself locates the gain in an added element** (a persistent knowledge base, a
separately-trained judge/grounding model, an external verification classifier) **and explicitly
diagnoses failure when the "element" is faked by role-prompting the same frozen model** (self-critique
loops, same-model reflection). This *confirms* the main thesis in a domain the project has not yet
mined, with one genuinely ambiguous case (RegionFocus, #6) that stress-tests the element/usage-pattern
boundary itself.

## Claims

### 1. AppAgent — exploration-built knowledge base as a persistent element

- **Recognized problem:** smartphone-app operation without backend/API access; the agent must learn
  UI affordances (what a button does) that are not recoverable from a single screenshot.
- **Genealogy:** origin **VLM**, native to the GUI-agent domain; v1 introduced autonomous
  exploration, v2 (2408.11824) added a structured, RAG-retrieved knowledge base.
- **Training-free vs fine-tuned:** training-free — the base VLM's weights are untouched; what
  changes is an external structured document store.
- **Three-axis class + verdict:** **element** (knowledge connector). The knowledge base is new
  information not recoverable from any one prompt to the frozen model — verdict: gain comes from a
  new-info element, not a usage pattern.
- **Fence tag:** cross-session-accumulating (the KB persists and grows across tasks/sessions).
- **Omni role:** n/a here (VLM, not omni) — analogous speech role would be **hybrid** (the omni
  model both writes and later reads the KB).
- **Transfer candidate to speech:** a persistent "dialogue-strategy / user-preference knowledge base"
  built by autonomous exploration of a voice-agent's own tool surface (e.g., which phrasing of a
  DB-query slot-fill actually succeeds in tau2-bench-style environments), retrieved via RAG at
  inference time — this is the direct GUI-methodology analog of the archive's S2 "skills as
  verified routines" design, but for *tool-affordance discovery* specifically.
- **VLM-known-failure-when-transferred:** the KB goes stale when the UI changes (app updates change
  button semantics) and v2's RAG retrieval can pull an outdated or wrong-context entry; the speech
  analog is a voice-agent tool schema changing (API version bump) without the KB being invalidated —
  no re-verification-on-drift mechanism is demonstrated in the GUI literature.
- **URL:** https://arxiv.org/abs/2312.13771 (AppAgent, 2023-12-21) and https://arxiv.org/abs/2408.11824
  (AppAgent v2, 2024-08-21). **Recency caveat:** both versions precede the 2025-01..2026-07 window
  (v1 by ~13 months, v2 by ~5 months); included as the necessary genealogy root for the KB-as-element
  pattern this lane tracks, tagged accordingly — same treatment as claim #3's Mobile-Agent-v2 citation
  and the Genealogy note's Mind2Web/WebArena. No in-window paper was found that introduces this
  specific KB-as-element mechanism fresh, so the root is cited directly rather than dropped.
- **Delta:** NEW (mechanism not previously cited in the wiki), but see recency caveat above — verify
  in Stage 2 whether an in-window successor/replication exists before leaning on this as a fresh 2025+
  data point.

### 2. Agent Workflow Memory (AWM) — reusable-workflow extraction as element, ICML 2025

- **Recognized problem:** web agents re-derive the same multi-step routine (e.g., "search flight →
  filter by price → book") from scratch on every task, wasting exploration and failing on
  compositional long-horizon tasks.
- **Genealogy:** origin **VLM/LLM-web-agent**, native; arXiv:2409.07429, ICML 2025 poster.
- **Training-free vs fine-tuned:** training-free — workflows are induced text artifacts fed back
  into the prompt/context, not gradient updates.
- **Three-axis class + verdict:** **element** (memory/knowledge connector: reusable workflow text
  extracted from past successful trajectories is new information the frozen model did not have).
  Evaluated on Mind2Web and WebArena.
- **Fence tag:** cross-session-accumulating (offline induction from training examples) with an
  online variant (induced from test-time trajectories) — both are explicitly the accumulating case
  the project's fence tags exist to separate from single-session use.
- **Omni role:** n/a (VLM/web); speech analog would be **brain**-side memory (informs planning).
- **Transfer candidate to speech:** extract reusable *dialogue/task routines* from successful
  voice-agent sessions (e.g., "confirm slot X before calling tool Y" patterns that resolved
  ambiguity) and re-inject them as workflow snippets for future sessions — a concrete, previously
  unlisted candidate mechanism for the archive's S2 "procedural skill library" tier.
- **VLM-known-failure-when-transferred:** none specific to AWM was found documented (its own
  paper reports gains, not failure modes); the general failure mode from #7/#8 below (memory that
  encodes *wrong* routines gets reinforced) applies by composition and is the open risk to flag.
- **URL:** https://arxiv.org/abs/2409.07429 (Agent Workflow Memory, ICML 2025).
- **Delta:** NEW.

### 3. Mobile-Agent-v2 — multi-agent role split as usage pattern, with one embedded element

- **Recognized problem:** single-agent long-horizon mobile GUI operation loses track of task
  progress and drifts from the original instruction.
- **Genealogy:** origin **VLM**, native; arXiv:2406.01014 (2024, precedes window but is the
  necessary genealogy root for v3 below, tagged accordingly).
- **Training-free vs fine-tuned:** training-free multi-agent prompting scaffold over one (or a
  small set of) frozen VLM backbone(s).
- **Three-axis class + verdict:** **mixed**. The Planning/Decision/**Reflection** agent split is a
  **usage pattern** — three roles are three prompts over essentially the same underlying model
  family, and the "reflection agent" role is exactly the same-model-critique-as-verifier
  construction the project's thesis predicts is weak. But the framework also adds an explicit
  **memory unit** tracking task progress/history — that piece is a genuine element (persistent
  state external to any single prompt).
- **Fence tag:** single-session (task-progress memory does not persist across separate user
  sessions in the base design).
- **Omni role:** n/a (VLM); speech analog of the reflection role = **hybrid** acting as pseudo-brain
  self-critic.
- **Transfer candidate to speech:** the memory-unit-for-task-progress piece (not the reflection-role
  piece) is the transferable element — an explicit external task-state tracker for multi-turn voice
  agentic tasks, separate from the dialogue-history context window.
- **VLM-known-failure-when-transferred:** Mobile-Agent-v3 (below) and the memory-confabulation
  literature (#8) both diagnose that a same-model "reflection agent" can misjudge its own actions as
  successful/unsuccessful without external ground truth — i.e., the role-based verifier component
  specifically is the fragile part, not the memory-unit component.
- **URL:** https://arxiv.org/html/2406.01014v1.
- **Delta:** NEW (not previously cited in the wiki's agent/GUI lanes).

### 4. Mobile-Agent-v3 / GUI-Owl — fine-tuned foundation model + multi-agent framework

- **Recognized problem:** prior multi-agent GUI frameworks (v2) plateau because the underlying VLM
  backbone itself is not specialized for GUI perception/grounding.
- **Genealogy:** origin **VLM**, native; arXiv:2508.15144 (2025-08).
- **Training-free vs fine-tuned:** **fine-tuned** — Mobile-Agent-v3 is built on GUI-Owl, a
  foundation model whose weights are specifically trained (not merely prompted) for GUI grounding,
  wrapped in a 4-agent orchestration (knowledge evolution, planning, execution, reflection).
- **Three-axis class + verdict:** **element** (the base-model fine-tuning) plus **usage pattern**
  (the 4-agent role split on top). Explicit contrast case: the literature's own framing is that the
  orchestration alone (v2, training-free) plateaus, and the reported jump comes with the new
  fine-tuned backbone — i.e., even inside GUI-agent literature, authors attribute capability gains to
  the model change, not the added roles.
- **Fence tag:** cross-session-accumulating (knowledge-evolution component).
- **Omni role:** n/a (VLM).
- **Transfer candidate to speech:** none directly training-free-relevant (this is a fine-tuning
  result) — cited here as a genealogy/contrast anchor, not a transfer candidate.
- **VLM-known-failure-when-transferred:** demonstrates the general risk that multi-agent-role
  papers can bundle a genuine element (fine-tuned backbone) with a usage-pattern (role split) and
  report the sum as if the orchestration itself were the cause — a methodological caution for
  reading any GUI/computer-use "multi-agent" result.
- **URL:** https://arxiv.org/html/2508.15144v2.
- **Delta:** NEW.

### 5. GTA1 — a genuinely separate judge model for test-time action selection

- **Recognized problem:** at inference, a GUI agent's single action proposal is often mis-grounded;
  naive repeated sampling with same-model self-selection does not reliably pick the correct one.
- **Genealogy:** origin **VLM**, native; arXiv:2507.05791 (2025-07, Salesforce AI Research).
- **Training-free vs fine-tuned:** **not training-free** — the grounding model is RL-trained, and
  critically the **judge model is a separate model** from the proposer, evaluating multiple sampled
  candidate action proposals and selecting among them.
- **Three-axis class + verdict:** **element** (verifier-as-tool: a distinct trained model, not a
  role prompt over the same frozen weights, performing the selection) reporting SOTA on grounding
  and agent-execution benchmarks. This is the domain's own working instance of the thesis's
  "verifier-as-tool = a real element" fork, as opposed to "verifier-as-role = usage pattern/weak."
- **Fence tag:** single-session (per-step selection, no cross-session persistence).
- **Omni role:** n/a (VLM); analog = **brain**-external judge, distinct weights from the
  perception/action model.
- **Transfer candidate to speech:** a separately-trained (not just separately-prompted) judge model
  for best-of-N selection over candidate ASR/ST/agentic-action outputs — stronger than a
  same-model critique prompt, and distinct from W1's frozen-omni-as-reward machinery in that the
  judge here is its own trained model, not the same frozen backbone in a different role.
- **VLM-known-failure-when-transferred:** the separate-judge approach requires RL training data for
  the judge itself — the training-free cell (frozen judge, no RL) is not what GTA1 reports; the
  comparison point (same-model role-based judging) is exactly what the archive's X3 lane already
  shows failing in text/VLM self-verification (arXiv:2402.08115).
- **URL:** https://arxiv.org/abs/2507.05791.
- **Delta:** NEW; CONFIRMS (verifier-as-tool > verifier-as-role fork) alongside X3's
  self-verification-limitations claims.

### 6. RegionFocus / Visual Test-time Scaling — the ambiguous boundary case

- **Recognized problem:** GUI grounding on dense/professional interfaces fails because the target
  element occupies a tiny fraction of a high-resolution screenshot; a frozen VLM's attention is
  diluted by irrelevant screen regions.
- **Genealogy:** origin **VLM**, native; arXiv:2505.00684 (2025-05, ICCV 2025).
- **Training-free vs fine-tuned:** **training-free** — applied directly to frozen VLMs (UI-TARS,
  Qwen2.5-VL) with no weight updates; +28%+ on ScreenSpot-Pro, +24%+ on WebVoyager, 61.6%
  ScreenSpot-Pro SOTA with Qwen2.5-VL-72B.
- **Three-axis class + verdict:** **genuinely ambiguous — the stress-test case for the framework.**
  On its face this is a **usage pattern** (an inference-time procedure: iteratively zoom into a
  candidate region and re-query the same frozen model). But the zoom-in step actively changes *what
  visual information is available to the model* (a cropped, higher-effective-resolution view the
  model did not have access to in its first pass) — arguably a **connector/tool-element** (an image
  op that expands perceptual input), not pure role-relabeling. Verdict: **this method does not cleanly
  fall on either side** — it is evidence that "usage pattern" and "element" are not always separable
  when the pattern itself manipulates the input rather than just re-asking the same question.
- **Fence tag:** single-session.
- **Omni role:** n/a (VLM); nearest omni analog = **sensor**-side operation (an audio equivalent
  would re-segment/re-sample the *raw* audio, not just re-prompt on the same features).
- **Transfer candidate to speech:** the direct analog is **not** re-prompting on the same features
  but an active "zoom" on the audio signal itself — e.g., iteratively re-extracting a higher-quality
  or narrower-band segment (isolating a speaker via source separation, re-sampling a suspected
  entity span at higher temporal resolution) before re-querying — a genuinely new information
  input, not a text-only usage pattern. This reframing itself is a useful test of the thesis: if
  the audio-domain analog is done as "zoom the model's attention over the same transcript" it will
  likely fail as a usage pattern; if done as "extract new signal" it is a connector/element.
- **VLM-known-failure-when-transferred:** RegionFocus's own gains are largest on ScreenSpot-Pro
  (professional/dense UIs) — precisely because these have small, spatially-separable targets, a
  condition without a clean audio-domain equivalent (audio does not have a 2D spatial layout);
  naive translation to "zoom into a spectrogram region" has not been demonstrated and may not
  carry the same information gain since spectrogram regions are not semantically discrete the way
  UI widgets are.
- **URL:** https://arxiv.org/abs/2505.00684.
- **Delta:** NEW; this claim itself functions as a REFUTES-flag against treating "usage pattern" and
  "element" as a clean binary — recorded as a caveat on the main thesis's operationalization, not a
  refutation of the thesis's substance (the new information is still real, just delivered through an
  inference *procedure* rather than a separately-stored artifact).

### 7. "Naive Visual Memory is Not Enough" — memory as element does not uniformly help

- **Recognized problem:** does adding visual (screenshot) memory to a GUI agent actually fix its
  failure modes, or trade one failure mode for another?
- **Genealogy:** origin **VLM**, native; arXiv:2606.14106 (2026-06), Seoyoung Choi et al.
- **Training-free vs fine-tuned:** training-free memory augmentation (storing/retrieving past
  screenshots) evaluated on OSWorld.
- **Three-axis class + verdict:** **element** (visual memory is new information across time steps)
  with a **negative/constraint finding**: full-image memory reduces state-level failures
  (cognitive/visual-misunderstanding) but *increases* action-level failures — hidden-operation
  blindness +11.7pp and grounding error +8.6pp on OSWorld — because stored screenshots add
  task-irrelevant visual cues that distract from precise coordinate grounding. Verdict: adding a
  memory element is not unconditionally beneficial; its value is task/failure-mode-dependent, and a
  naive full-fidelity memory format can actively hurt a different capability axis.
- **Fence tag:** single-session (within-episode visual memory in the reported design).
- **Omni role:** n/a (VLM); nearest analog = **sensor** memory (raw perceptual buffer) as opposed to
  **brain**-level distilled/symbolic memory.
- **Transfer candidate to speech:** a caution rather than a recipe — raw-audio (or raw-spectrogram)
  turn history as agent memory (as opposed to distilled transcript/state summaries) may similarly
  trade a perceptual-understanding gain for a precision/grounding loss (e.g., worse entity-span
  localization) in long-horizon voice-agent tasks; this is a directly relevant negative to weigh
  against W4's plan to index memory on raw audio rather than ASR text.
- **VLM-known-failure-when-transferred:** the paper's own proposed fix ("recovery-aware
  verification memory") only partially addresses the cascading effect — it does not fully recover
  the state-level gains without the action-level cost, i.e., the tradeoff is not fully solved even
  within the VLM/GUI domain, so speech should not assume the analogous tradeoff is either.
- **URL:** https://arxiv.org/html/2606.14106.
- **Delta:** NEW.

### 8. "Honest Lying" — memory confabulation from reflexive self-critique loops

- **Recognized problem:** agents that reflect on their own past actions (Reflexion-style
  architectures) sometimes construct and act on false narratives of what actually happened.
- **Genealogy:** origin **VLM/LLM-agent**, native; arXiv:2605.29463 (2026), Dixit, Kamal & Oates.
- **Training-free vs fine-tuned:** training-free — the confabulation arises purely from the
  self-reflection *prompting* loop over a frozen model, not from any weight change.
- **Three-axis class + verdict:** **usage pattern**, and the paper's controlled experiments show it
  **failing**: repeated self-reflection cycles produce systematically distorted, high-confidence
  accounts of the agent's own behavior that get written into memory and acted on in later steps —
  a multi-trial failure distinct from single-turn hallucination (the false content is stored,
  retrieved, and reinforced). Verdict: this is direct empirical evidence for the thesis's prediction
  that **verifier/critic-as-role over one frozen model is provably bounded and here actively
  degrades** rather than merely failing to help.
- **Fence tag:** cross-session-accumulating (confabulated "memories" persist and compound across
  reflection cycles — precisely the failure mode the archive's S1/S2 lanes flag for uncurated
  memory writes).
- **Omni role:** n/a (VLM/LLM); speech analog = **hybrid** self-reflecting on its own prior
  turns/actions.
- **Transfer candidate to speech:** a direct negative-transfer warning for any voice-agent design
  that has the omni model reflect on/summarize its own prior dialogue turns into long-term memory
  without an external verification gate — this is exactly the failure mode the archive's S2 control
  law (verifiable-reward acceptance gate) is designed to prevent, now with direct VLM/LLM-agent
  empirical evidence of the failure it prevents.
- **VLM-known-failure-when-transferred:** n/a — this claim *is itself* the transferred failure
  mode; the open question is whether it is worse or better in speech, where the omni model's
  self-report of "what the user said" could confabulate in the same way an LLM confabulates "what I
  did," compounding with ASR error.
- **URL:** https://arxiv.org/pdf/2605.29463.
- **Delta:** NEW; CONFIRMS the thesis's verifier-as-role-is-weak prediction with a concrete failure
  mechanism (confabulation) not previously named in the wiki's self-verification claims (X3-05/06
  cite task-performance degradation; this adds the memory-corruption pathway specifically).

### 9. "Visual Confused Deputy" — grounding-failure rate and external dual-channel verification

- **Recognized problem:** computer-use agents (CUAs) execute actions based on misperceived screen
  states; how often does this happen, and can an external check catch it before execution?
- **Genealogy:** origin **VLM**, native; arXiv:2603.14707 (2026-03), Liu, He, Liu, Luo, Zhang, Chen.
- **Training-free vs fine-tuned:** training-free — both the vulnerability measurement and the
  proposed defense operate on/around a frozen CUA without retraining it.
- **Three-axis class + verdict:** **constraint** (perception-fidelity failure rate, a base-model
  quality) plus **element** (the defense). Measured baseline: **56.7% of CUA click actions miss
  their intended on-screen target**, and on professional GUIs (ScreenSpot-Pro-class) grounding
  accuracy is only **18.9%**. The proposed defense, "Dual-Channel Contrastive Classification," is
  explicitly **two independent classifiers operating outside the agent's own perceptual loop** (an
  image-channel classifier against a visual danger/permitted knowledge base, a text-channel
  classifier against an intent knowledge base, OR-gated) — reaching **F1 = 0.915** on
  ScreenSpot-Pro and **F1 = 1.0** on neutral-button adversarial cases where the image channel alone
  fails. Verdict: the *working* defense is architecturally a verifier-as-tool (separate models,
  separate objective, outside the loop), not a verifier-as-role add-on to the same CUA.
- **Fence tag:** single-session (per-action veto check).
- **Omni role:** n/a (VLM); analog = **sensor**-adjacent external check, not the acting **brain**.
- **Transfer candidate to speech:** the 56.7%-miss-rate statistic is itself a strong argument for
  building an analogous external, out-of-loop check for voice-agent tool calls (e.g., an
  independent classifier verifying a parsed slot value/intent against the raw audio before a
  destructive tool call executes) rather than trusting the acting omni model's own confidence — a
  concrete "verifier-as-tool" design pattern with a quantified before/after (F1 0.915) to benchmark
  a speech analog against.
- **VLM-known-failure-when-transferred:** the defense depends on having pre-built visual/text
  knowledge bases of "dangerous" vs "permitted" states for the specific application — this
  requires domain curation effort that does not automatically port; a speech analog would need an
  equivalent curated set of "high-risk" intents/slot-values per deployed tool surface.
- **URL:** https://arxiv.org/html/2603.14707.
- **Delta:** NEW; strengthens the thesis's verifier-as-tool fork with a concrete adversarial/security
  framing not previously in the wiki.

### 10. VerificAgent — external, weight-untouched memory-integrity verification

- **Recognized problem:** computer-use agents that accumulate memory over time are vulnerable to
  memory poisoning/corruption that then silently biases future actions; how to catch this without
  retraining the agent.
- **Genealogy:** origin **VLM/agent-oversight**, native; arXiv:2506.02539, Nguyen, Desai, Anwar,
  Shaik, Suryanarayanan, Chowdhary.
- **Training-free vs fine-tuned:** training-free — an explicitly **separate, external oversight
  component** that audits memory contents independently of the agent's action-generation process
  and does not alter the agent model's weights.
- **Three-axis class + verdict:** **element** (a genuine new connector: a domain-specific memory
  verification system, distinct from the acting model). Verdict: this is architecturally the same
  "verifier as tool, not role" pattern as #5 and #9, applied specifically to the memory-integrity
  problem rather than the action-grounding problem.
- **Fence tag:** cross-session-accumulating (the whole point is auditing memory that persists and
  compounds across sessions).
- **Omni role:** n/a (VLM); analog = an external auditor distinct from **brain**.
- **Transfer candidate to speech:** directly relevant to any design that gives an omni voice agent
  a persistent cross-session memory (per the archive's S2 memory design) — an external,
  training-free verification layer specifically for detecting poisoned/corrupted memory entries
  (e.g., an injected-audio adversarial instruction that got written into long-term user-preference
  memory) before it influences future turns.
- **VLM-known-failure-when-transferred:** the paper frames this as "scalable oversight," implying
  the verification system's own reliability/coverage is not itself formally bounded — a general
  caution that adding a verifier does not eliminate risk, only shifts where the residual risk sits
  (in the verifier's own blind spots).
- **URL:** https://arxiv.org/pdf/2506.02539.
- **Delta:** NEW.

### 11. OSWorld — execution-based (ground-truth state) evaluation as the verifiable-reward element

- **Recognized problem:** GUI-agent benchmarks that rely on the agent's own self-report of success,
  or on LLM-judge scoring, cannot be trusted; task success needs to be checked against actual
  system/file/OS state.
- **Genealogy:** origin **VLM**, native; arXiv:2404.07972 (2024-04, NeurIPS 2024), Xie et al.
- **Training-free vs fine-tuned:** n/a (benchmark, not a method) — but its evaluation protocol is
  itself an **element**: execution-based checks of real OS/file/application state, not a model
  self-judgment or role-based verifier.
- **Three-axis class + verdict:** **constraint/methodology reference** — a genuine verifiable-reward
  design (the GUI-domain equivalent of the project's on-disk tau2-bench DB-state pass@k). Reported
  human-vs-model gap: humans complete **72.36%** of the 369 real-world tasks; the best evaluated
  model manages only **12.24%**, with failures concentrated in GUI grounding and operational
  knowledge — i.e., a large, still-open capability gap that execution-based (not model-judged)
  scoring makes trustworthy.
- **Fence tag:** n/a (benchmark).
- **Omni role:** n/a.
- **Transfer candidate to speech:** confirms (does not merely suggest) the design already adopted
  by this project's on-disk benchmark set — tau2-bench's verifiable DB-state pass@k is architecturally
  the direct speech-domain analog of OSWorld's execution-based evaluation; this is a CONFIRMS-type
  cross-domain validation that the project's existing benchmark choice follows the same "ground
  truth, not model-judgment" principle the GUI-agent field converged on independently.
- **VLM-known-failure-when-transferred:** n/a (this is the benchmark methodology being praised, not
  a failure); the failure risk is on the *agent* side — the 12.24% best-model number is itself
  evidence that GUI grounding is a hard, unsolved constraint, not evidence against the benchmark
  design.
- **URL:** https://arxiv.org/abs/2404.07972. **Recency caveat:** predates the 2025-01..2026-07 window
  (2024-04, NeurIPS 2024) — same situation as Mind2Web/WebArena in the Genealogy note below, but cited
  here as a first-class claim (with quantitative numbers) rather than moved to genealogy-only, because
  the execution-based-eval methodology point is load-bearing for the CONFIRMS delta and no in-window
  paper supersedes OSWorld itself as the citable source for the 72.36%/12.24% figures.
- **Delta:** CONFIRMS (the project's existing tau2-bench choice, via independent cross-domain
  convergence on execution-based verification).

### 12. Agent S2 — specialist grounding experts inside a "multi-agent" framing

- **Recognized problem:** monolithic single-VLM computer-use agents plateau on precise GUI
  localization and on planning across widely varying temporal scales (a single click vs. a
  50-step task).
- **Genealogy:** origin **VLM**, native; arXiv:2504.00906 (2025-04).
- **Training-free vs fine-tuned:** mixed — the Manager/Worker planning modules are prompted
  (training-free orchestration), but the "Mixture-of-Grounding" specialist **grounding experts**
  are separately specialized models composed into the pipeline, not role-prompts over one backbone.
- **Three-axis class + verdict:** **element** (the specialist grounding experts are the load-bearing
  addition) framed in the paper as "multi-agent"/"compositional" — a caution that "multi-agent"
  branding in this literature often bundles a genuine element (specialist models) with orchestration
  (usage pattern), similar to #4. Reported gains: **18.9%** and **32.7%** relative improvement over
  Claude Computer Use and UI-TARS on OSWorld (15-step/50-step), **52.8%** relative on
  WindowsAgentArena, **16.52%** relative on AndroidWorld.
- **Fence tag:** single-session (per the reported architecture; no persistent cross-session store
  described in the summarized abstract).
- **Omni role:** n/a (VLM); analog = specialist **sensor**-adjacent grounding models feeding a
  **brain**-level planner.
- **Transfer candidate to speech:** the "compose a generalist planner with specialist perception
  experts" pattern maps to composing a frozen omni planner with specialist frozen speech models
  (dedicated diarization/SER/entity-extraction models) as the grounding layer — distinguishable
  from, and likely more load-bearing than, a same-model "listen more carefully" role-prompt.
- **VLM-known-failure-when-transferred:** the paper's own framing (labeling specialist-model
  composition as "multi-agent") is itself a documented terminology risk — readers/reviewers should
  not credit the "agent" framing for gains that come from the specialist models.
- **URL:** https://arxiv.org/abs/2504.00906.
- **Delta:** NEW.

### 13. UI-TARS / UI-TARS-2 — fine-tuning (an element via weight change) as the actual boundary-crosser

- **Recognized problem:** prompting a general-purpose VLM to act as a GUI agent underperforms a
  model natively trained end-to-end for GUI perception/action.
- **Genealogy:** origin **VLM**, native; arXiv:2501.12326 (UI-TARS, 2025-01, ByteDance),
  arXiv:2509.02544 (UI-TARS-2, 2025-09).
- **Training-free vs fine-tuned:** explicitly **fine-tuned** — UI-TARS-2's own technical report
  frames its advance as a "data flywheel," a "stabilized multi-turn RL framework," and a hybrid GUI
  training environment; this is a weight-changing pipeline, not an inference-time procedure.
- **Three-axis class + verdict:** **element** (the fine-tuned weights themselves are the
  boundary-crosser) — recorded here explicitly as the **contrast case** to every training-free
  usage-pattern claim above: in this domain too, the SOTA-defining jumps (UI-TARS vs its own
  earlier prompted-VLM baselines, and Mobile-Agent-v3/GUI-Owl vs Mobile-Agent-v2) are attributed by
  their own authors to a fine-tuned/RL-trained backbone, not to orchestration alone.
- **Fence tag:** n/a (gradient-trained, out of the training-free fence).
- **Omni role:** n/a (VLM).
- **Transfer candidate to speech:** none directly (fine-tuning is out of scope for the project's
  training-free thesis) — cited as the genealogy anchor establishing that, even in the reference
  domain, "usage pattern over a frozen backbone" is consistently the *weaker* lever relative to
  "new element via fine-tuning," which is exactly what the project's thesis predicts about
  usage patterns generally (they are bounded by, not a substitute for, the underlying model's
  capability).
- **URL:** https://arxiv.org/abs/2501.12326 and https://arxiv.org/html/2509.02544v1.
- **Delta:** NEW; CONFIRMS (usage-pattern-is-bounded-by-backbone) by contrast.

### 14. "An Illusion of Progress?" — reported GUI/web-agent progress is over-optimistic

- **Recognized problem:** are the large reported capability jumps for web/GUI agents real, or
  artifacts of benchmark methodology (static, offline benchmarks that don't reflect live-web
  variability)?
- **Genealogy:** origin **VLM/web-agent**, native; arXiv:2504.01382 (COLM 2025), Xue, Qi, Shi, Song,
  Gou, Song, Sun, Su.
- **Training-free vs fine-tuned:** n/a (a critical/measurement paper, not a method).
- **Three-axis class + verdict:** **negative/first-class finding.** The paper's own words: current
  offline evaluations "depict a very different picture" than a more rigorous live benchmark
  (Online-Mind2Web, 300 tasks/136 sites), concluding there has been **"over-optimism in previously
  reported results."** It also introduces an LLM-as-judge automated evaluator reaching ~85%
  agreement with human raters — itself a usage-pattern (LLM-judge) used for *evaluation
  infrastructure*, not for the agent's own capability, so it should not be read as evidence that
  LLM-judge-as-verifier works for the agent loop itself.
- **Fence tag:** n/a.
- **Omni role:** n/a.
- **Transfer candidate to speech:** a direct methodological caution to weigh against any
  training-free speech/omni-agent result reported only on static or narrow benchmarks — the GUI/web
  field's own retrospective finding is that its rosier numbers did not hold up under a harder, more
  realistic evaluation; the project's Stage-1→Stage-2 escalation (small-n directional-only →
  pre-registered large-sample) is precisely the discipline this paper argues the field skipped.
- **VLM-known-failure-when-transferred:** n/a — this claim is itself the general-purpose caution.
- **URL:** https://arxiv.org/abs/2504.01382.
- **Delta:** NEW; this is a first-class **negative** finding for the archive (evidence that the
  reference domain's own reported gains are contested, reinforcing the project's insistence on
  Stage-2 pre-registered validation before trusting Stage-1 numbers).

## Negatives / empty cells (first-class)

- **No GUI/computer-use agent memory, skill-library, or multi-agent orchestration method identified
  in this search has been applied to, or evaluated on, any voice-agent benchmark** (tau2-bench,
  eva-bench, soulx-duplug, audiomc, voiceassistant-eval, voicebench, uro-bench, vocalbench) as of
  2026-07 — the transfer is entirely unstarted in the published literature, consistent with the
  archive's L4 negatives (N1/N2: no published pass@k or prompt-opt on any voice-agent benchmark).
- **No audio-domain analog of Set-of-Mark-style input-space intervention or of RegionFocus-style
  active re-sampling of the raw signal** (as opposed to re-prompting on the same features) was
  found for GUI-style "zoom and re-verify" test-time scaling — the ambiguous element/usage-pattern
  case in claim #6 remains untested in speech in either direction.
- **No same-model-role verifier was found to outperform a separately-trained/separately-instantiated
  judge or external classifier** anywhere in this lane's sources (#5, #9 both show the working
  defense is architecturally separate from the acting model) — no counterexample surfaced where
  role-prompting alone matched a genuine external verifier's numbers.
- **Memory confabulation (#8) has no published measurement in any GUI/computer-use benchmark of
  how often it occurs "in the wild"** (the paper is a mechanism/case study, not a benchmark
  prevalence study) — the severity of the failure mode at scale is itself an open/empty cell even
  within the VLM/GUI domain, let alone speech.

## Genealogy note

Mind2Web (arXiv:2306.06070, NeurIPS 2023 Spotlight) and WebArena (ICLR 2024) are the two web-agent
benchmark genealogy roots underlying claim #2 (AWM) and much of the broader GUI/web-agent
literature surveyed here; both predate the 2025-01..2026-07 recency window and are cited only as
genealogy, per the lane's citation rules.

## Verifier notes (adversarial pass, 2026-07-06)

**Method:** WebFetch on 10 of the 17 distinct arXiv URLs cited (claims #1, #2, #5, #6, #7, #8, #9,
#10, #11, #12, #13-UI-TARS-2), cross-checked with WebSearch for the ones with the least-plausible-
looking IDs (very recent 2026 dates: #7, #8, #9) and for the AWM venue claim.

**URL / claim accuracy:** All 10 spot-checked URLs resolve to real papers whose title, authors, and
core claims match the lane's description. All quantitative figures independently re-derived from
primary or near-primary sources and confirmed exact:
- #7: OSWorld hidden-operation-blindness 67.1%→78.8% (+11.7pp) and grounding error 27.5%→36.1%
  (+8.6pp) — confirmed verbatim from the paper's results section (via `arxiv.org/html/2606.14106v1`).
- #9: 56.7% CUA click miss-rate and 18.9% ScreenSpot-Pro-class grounding accuracy both confirmed
  present in the paper (the miss-rate and the 18.9% figure are from different tables/baselines than
  the 43.6%/0.8% numbers a fast summarization pass initially surfaced from the same paper — not a
  contradiction, just multiple reported baselines; F1=0.915 and F1=1.00 also confirmed).
- #11 OSWorld: 72.36% human / 12.24% best-model confirmed exact.
- #12 Agent S2: 18.9%/32.7%/52.8%/16.52% relative-improvement figures confirmed exact.
- #2 AWM: ICML 2025 poster status confirmed independently (icml.cc/virtual/2025/poster/45496,
  proceedings.mlr.press/v267/wang25bx.html) despite the arXiv preprint itself predating the window
  (see recency note below).
- No invented, dead, or misattributed URL found; no unsupported/fabricated statistic found among the
  claims checked. The three most recent-looking IDs (#7 `2606.14106`, #8 `2605.29463`,
  #9 `2603.14707`) are all real, resolving papers, not hallucinations — this was the a priori highest-
  risk category and it came back clean.

**Recency-window inconsistency found and fixed:** claim #1 (AppAgent, both v1 2312.13771 and v2
2408.11824) and claim #11 (OSWorld, 2404.07972) cite pre-2025-01 papers as first-class, "Delta: NEW"
/ "Delta: CONFIRMS" claims without the "precedes window, tagged as genealogy root" caveat that the
lane already applies to claim #3 (Mobile-Agent-v2, 2406.01014) and to Mind2Web/WebArena in the
Genealogy note. This was an inconsistent application of the lane's own stated citation rule — fixed
in place (see the two `**Recency caveat:**` insertions above) rather than deleting the claims, since
both are load-bearing (KB-as-element genealogy; execution-based-eval methodology anchor) and no
in-window replacement was found for either during this pass. Flag for Stage 2: confirm whether an
in-window (2025+) successor paper exists for AppAgent's KB mechanism specifically, rather than
resting on the 2023/2024 originals.

**Framework-verdict spot-check (element vs. usage-pattern, new-info vs. read-out):** all 14 verdicts
are defensible under the "usage pattern over one frozen model = read-out" rule. Notably:
- #3, #4, #12 correctly split a single paper into element (fine-tuned backbone / specialist grounding
  models / memory unit) + usage pattern (role-prompt orchestration) rather than crediting the whole
  paper to one bucket — this is the correct move where the literature itself bundles both.
- #6 (RegionFocus) is the one case that does not cleanly fit either bucket, and the lane says so
  explicitly rather than forcing a call — this is the right epistemic move, not a miscall. Its
  argument (a zoom/crop operation changes what visual information reaches the frozen model, so it
  isn't pure re-prompting) is sound and correctly flagged as a stress test of the framework's own
  boundary rather than a counterexample to the thesis.
- #8 (Honest Lying) is correctly scored as usage-pattern-fails (self-reflection loop over one frozen
  model, empirically shown to degrade) — the strongest direct confirmation in the lane.
- No case was found where a same-model role-prompt was mislabeled as an "element," or where a
  genuinely separate model/component was mislabeled as a mere "usage pattern."
- Minor unconfirmed-but-plausible detail: claim #4's abstract-only fetch did not surface the specific
  "4-agent (knowledge evolution / planning / execution / reflection)" framing verbatim — likely just
  an abstract-vs-full-paper visibility gap given Mobile-Agent-v3's known lineage from v2's role
  structure, not treated as an error, but worth a full-text check before Stage 2 reliance.

**Recency and negatives (2025-01..2026-07):** 12 of 14 claims' primary in-window citations are dated
correctly within the window (earliest in-window: #13 UI-TARS, 2025-01; latest: #7, 2026-06); the two
exceptions (#1, #11) are addressed above. The "## Negatives / empty cells" section is present and
first-class (4 distinct negatives, not folded into a single vague caveat), and correctly cross-links
to the archive's own negatives (L4 N1/N2) rather than treating this lane's negatives as isolated.
