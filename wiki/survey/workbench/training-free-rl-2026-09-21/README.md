# Optimisation principles behind training-free RL / inference-time policy improvement

Owner-facing survey memo, 2026-09-21. Scope: the optimisation *principles* available when the policy
is a frozen LLM behind an API boundary and no weight may change. The owner already named two — group
rollout sampling plus an update operator over an experience store, and pruning pipeline components to
find Pareto-optimal effect/cost points. This memo places both inside seven families and maps each to
the SAEA base. Every claim comes from an arXiv abstract or publisher page I opened; where a venue was
not printed on that page I cite the arXiv id only. Unverified items are listed before the references.

---

## 1. Experience libraries and semantic advantage

**(a)** The frozen model's output distribution can be shifted by a *token prior* — text in context —
instead of by gradients. Training-Free GRPO keeps the GRPO skeleton (a group of rollouts per problem,
an advantage within the group) but replaces the *numerical* advantage with a **group relative semantic
advantage**, a natural-language contrast between better and worse rollouts, and replaces the policy
update with an edit to an experience library (Cai et al., arXiv:2510.08191, 2025). Reflexion is the
same idea at episode scale: verbal reflection in episodic memory replaces the policy gradient (Shinn
et al., arXiv:2303.11366, 2023).

**(b)** Optimised: a persistent text store — distilled insights (Training-Free GRPO, ExpeL, ACE),
reflection strings (Reflexion), validated code and strategies (Dynamic Cheatsheet, Voyager's skill
library), induced routines (Agent Workflow Memory). ExpeL also keeps a vector DB of successful
trajectories retrieved top-k, so the store is both rule set and demonstration pool (Zhao et al.,
AAAI-24).

**(c)** Labels divide the family. Training-Free GRPO needs "minimal ground-truth data" (a few dozen
items) and ExpeL a labelled task set; Dynamic Cheatsheet claims gains "without needing explicit
ground-truth labels or human feedback" (Suzgun et al., arXiv:2504.07952, 2025) and ACE "could adapt
effectively without labeled supervision and instead by leveraging natural execution feedback" (Zhang
et al., arXiv:2510.04618, 2025).

**(d)** Generate–reflect–curate loops. ACE separates generation, reflection and curation and adds a
*grow-and-refine* rule: structured incremental delta updates, never whole-context rewriting.

**(e)** ACE names the two failure modes that matter — **brevity bias** (summarising away the domain
detail that carried the gain) and **context collapse** (iterative rewriting eroding detail over
rounds). Cost is prefill: the store is paid on every row forever. A wrong stored insight is a
permanent regression, and intrinsic self-correction without external feedback can *degrade* reasoning
(Huang et al., ICLR 2024).

**(f) Mapping to SAEA.** Closest family to the base. SAEA already has the store (versioned pinned
views), the rollouts (grouped Solver sampling with a registered commit policy), the official scorer,
and the construction/discovery split that makes "gold during construction only" legitimate. Missing is
the *update operator*: today a view is authored, pinned, flown once. The Training-Free GRPO form maps
directly — per construction-pool row, sample N Solver rollouts, score them, take the best/worst pair,
ask the frozen core to state in words what distinguished them, apply that as a delta. ACE's warning is
sharper still: the L0/L1 index lost 7.4 pp, the brevity-bias signature (an index is a summary that
drops the detail the k=20 exemplars supplied). Prefer **additive deltas with per-item provenance** to
rewriting a view, so a harmful item can be ablated by id under the existing one-factor-cell discipline.

---

## 2. Prompt and instruction optimisation by LLM feedback

**(a)** The instruction string is a free parameter, optimisable without gradients — by treating the
LLM as a black-box optimiser over a scored trajectory of past candidates (OPRO; Yang et al.,
arXiv:2309.03409, 2023), or by constructing a *textual gradient*, a critique saying in which semantic
direction to edit (ProTeGi; Pryzant et al., EMNLP 2023; TextGrad; Yuksekgonul et al.,
arXiv:2406.07496, 2024).

**(b)** Optimised: free-form instructions per module, and in MIPRO jointly the instructions *and* the
few-shot demonstrations of every module of a multi-stage program (Opsahl-Ong et al., EMNLP 2024;
Khattab et al., arXiv:2310.03714, 2023).

**(c)** A scalar dev-set metric, so **gold labels are required** on the search set — though MIPRO needs
no *module-level* labels, only the end metric. GEPA is the exception in kind: it consumes the
natural-language trace (reasoning, tool calls, tool outputs), not only the scalar.

**(d)** Four sub-schools: beam search with bandit selection over textual gradients (ProTeGi);
backpropagation-shaped textual differentiation over a graph (TextGrad); evolutionary — EvoPrompt runs
a GA/DE over a prompt population (Guo et al., ICLR 2024), Promptbreeder additionally evolves its own
*mutation prompts* (Fernando et al., arXiv:2309.16797, 2023); and surrogate/Bayesian — MIPRO learns a
surrogate of the objective from stochastic mini-batch evaluation.

**(e)** Evaluation cost dominates — a dev-set pass per candidate, populations need many, and
over-fitting a small dev split is the standard failure. GEPA's advantage is sample efficiency: it
"outperforms GRPO by 6% on average and by up to 20%, while using up to 35x fewer rollouts", and beats
MIPROv2 by over 10% (Agrawal et al., ICLR 2026 Oral; arXiv:2507.19457).

**(f) Mapping to SAEA.** GEPA is the most transferable algorithm here and needs no new machinery.
(1) **Reflect on the trace, not the number** — SAEA seals per-row outputs under `runs/<run_id>/`, so
the Reviewer/Planner transcript of a failing row already is the richer signal GEPA argues for.
(2) **Pareto-frontier candidate selection** — keep not the best-average candidate but the set best on
*some* stratum, and recombine; SAEA already reports per-stratum tables (per-scenario SLURP, per-tier
A2T), so the frontier is computable from artefacts that exist. Cost asymmetry matters: a SAEA dev pass
is DEV-500/DEV-2000 rows of speech through a local core — GPU-hours, not API dollars — which argues
for GEPA/ProTeGi (tens of candidates) over EvoPrompt/Promptbreeder (populations × generations).

---

## 3. Demonstration and retrieval policy optimisation

**(a)** "Which exemplars to show" is an action with a learnable policy. Retrieving semantic near
neighbours beats random selection (KATE; Liu et al., arXiv:2101.06804, 2021), and the retriever can be
trained from the LM's own scoring of candidate prompts rather than from human labels (EPR; Rubin et
al., NAACL-HLT 2022).

**(b)** Optimised: the retrieval policy — key, scoring function, k, ordering. In Adaptive-RAG the
*amount* of retrieval is the action: none / single-step / multi-step, chosen per query complexity
(Jeong et al., NAACL 2024).

**(c)** EPR labels candidate exemplars by the LM's probability of the gold output given that exemplar —
gold to fit the selector, none at inference. Active Example Selection learns selection as a sequential
decision problem with RL from task reward (Zhang, Feng and Tan, EMNLP 2022). TRIPLE needs only an
evaluable score per candidate.

**(d)** Dense retrieval on LM-derived pseudo-labels; RL over selection sequences; and **fixed-budget
best-arm identification** in a multi-armed bandit when candidates are few and evaluation is expensive
(TRIPLE; Shi et al., NeurIPS 2024).

**(e)** The honest negative: Active Example Selection gave +5.8% on GPT-2 but "the improvement
diminishes on larger GPT-3 models" — a selector fitted against a weak reader need not transfer to a
strong one. Retrieval keys also echo: a key derived from the model's own draft mostly retrieves the
draft back.

**(f) Mapping to SAEA.** The base's largest admitted gain *is* a retrieval policy (speech-keyed
exemplars, k=20, +12.6 pp SLU-F1). Two moves. **TRIPLE-style best-arm identification over
knowledge-view variants**: SAEA evaluates one full sealed cell at a time, but a fixed-budget BAI
schedule over a handful of variants (k, key family, view family) spends the same GPU-hours separating
the best variant instead of measuring each precisely — the right statistical tool for "one experiment
in flight, n>=400". **Adaptive-RAG as the SUPPLY axis**: make retrieval depth a per-row action
conditioned on the Perception node's candidate-intent spread rather than a constant k, paying prefill
only on rows that need it.

---

## 4. Test-time compute and search

**(a)** Accuracy can be bought with inference compute, and the exchange rate depends on *how* it is
spent and on row difficulty. Snell et al. compare search against a dense process verifier versus
adaptive revision, and find a per-prompt "compute-optimal" allocation improves efficiency "by more
than 4x compared to a best-of-N baseline"; where a small model already has non-trivial success,
test-time compute can beat a 14x larger model (arXiv:2408.03314, 2024).

**(b)** Optimised: the search/verification budget and its allocation — sample count, tree width and
depth, revision rounds, stopping.

**(c)** Three tiers of signal. Label-free: self-consistency marginalises over sampled reasoning paths
(Wang et al., ICLR 2023). Learned verifier: best-of-N reranking (Cobbe et al., arXiv:2110.14168,
2021); process reward models on 800K *human* step labels (Lightman et al., arXiv:2305.20050, 2023) —
or on **automatically constructed** step supervision (Math-Shepherd; Wang et al., arXiv:2312.08935,
2023). Model-as-value: LATS uses LM value functions and self-reflection inside MCTS (Zhou et al.,
ICML 2024).

**(d)** Sampling plus aggregation; tree search (Tree of Thoughts, Yao et al., NeurIPS 2023; LATS); and
token-level reward-guided decoding — RAD rescales sampling probabilities with a unidirectional reward
model (Deng and Raffel, EMNLP 2023), controlled decoding trains a prefix scorer as a value function
for a frozen base and combines rewards at inference (Mudgal et al., ICML 2024), ARGS folds a reward
into the decoding step (Khanov et al., ICLR 2024).

**(e)** Two hard negatives. **Coverage ≠ selection**: coverage scales over four orders of magnitude of
samples, but "majority voting and reward models plateau beyond several hundred samples" absent an
automatic verifier (Brown et al., arXiv:2407.21787, 2024). **Non-monotonicity**: Vote and Filter-Vote
"can first increase but then decrease as a function of the number of LM calls", because more calls
help easy queries and hurt hard ones (Chen et al., arXiv:2403.02419, 2024). Reward-guided *decoding*
is unreachable behind a strict API boundary unless logits are exposed.

**(f) Mapping to SAEA.** Grouped Solver sampling already is best-of-N; its selection rule is the open
question. The base's logprob probe was NOT ADMITTED (min-token AUROC 0.69, 51% precision against a
legality judge at 67% free) — the Brown-et-al. selection ceiling appearing locally. So: treat N as a
*tuned* per-stratum parameter with a measured optimum rather than a constant (Chen 2024); measure the
Reviewer x3 ensemble's selection precision directly against the official scorer on the construction
pool, because a verifier below the noise floor makes extra samples cost-only; and take Math-Shepherd
as the template for a process signal needing no new annotation — step labels derived from whether a
prefix can still reach a correct final answer. Cost is already in the base's units (prefilled
tokens/row, GPU-h per 1,080 rows), so a Snell-style compute-optimal curve is directly constructible.

---

## 5. In-context RL and algorithm distillation

**(a)** An RL *algorithm* can live in the context window. Algorithm Distillation trains a causal
transformer on the across-episode learning histories of a source RL algorithm; the result "is able to
improve its policy entirely in-context without updating its network parameters" (Laskin et al.,
arXiv:2210.14215, 2022). In-Context Policy Iteration runs policy iteration with a frozen model: real
trajectories enter an experience buffer, prompt context is sampled from it, and model-generated
rollouts serve as the value estimate for greedy action selection (Brooks et al., arXiv:2210.03821,
2022; NeurIPS 2023).

**(b)** Optimised: the context itself as carrier of the learning history — no parameter, no template,
no curation step.

**(c)** Environment reward only, no gold outputs — but AD needs a *pretraining* corpus of learning
histories, a weight update at an earlier stage, hence unavailable for a frozen third-party core.

**(d)** Sequence modelling of learning histories (AD); Monte-Carlo policy iteration with LM-generated
rollouts as the environment model (ICPI).

**(e)** AD's in-context improvement is bounded by the source algorithm it distilled and by the context
window; ICPI was demonstrated on six *small control tasks*, each improvement step costing a
model-generated rollout.

**(f) Mapping to SAEA.** Treat this family as a *boundary statement*, not a method to adopt. What
transfers from ICPI is the structural insight that an experience buffer plus a rollout-based value
estimate suffices for policy iteration without gradients — which is what family 1 does in text. What
does not transfer is any expectation that the Qwen3-Omni core learns within or across episodes on its
own. Whatever improvement SAEA gets is carried by what the harness writes into the context between
rows, so the unit of learning is the pinned store version, never the episode.

---

## 6. Structure and workflow search

**(a)** The agent *graph* is the parameter. AFlow reformulates workflow optimisation as search over
code-represented workflows whose nodes are LLM invocations and whose edges are control flow, explored
with MCTS on execution feedback (Zhang et al., arXiv:2410.10762, 2024). ADAS goes one level up: a meta
agent programs new agents against an ever-growing archive of previous discoveries (Hu et al.,
arXiv:2408.08435, 2024).

**(b)** Optimised: node set, node order, control flow, and the tool set exposed at each node. DSPy
optimises prompts and demonstrations at fixed structure; AFlow/ADAS change the structure.

**(c)** A benchmark metric, so gold labels on a search set are required; execution feedback (errors,
tool outputs) supplements the scalar.

**(d)** MCTS over code edits (AFlow); archive-driven open-ended generation (ADAS); surrogate-guided
joint proposal (MIPRO).

**(e)** Every candidate graph costs a full benchmark pass. Tool-set size is a first-order confound any
structure search must control: LongFuncEval measures 7–85% degradation as the tool catalogue grows
from 8K to 120K tokens and 7–91% as tool responses lengthen (Kate et al., arXiv:2505.10570, 2025);
adaptive per-query shortlists beat fixed ones, matching 50-tool coverage while showing ~7 tools on
average (Repantis et al., arXiv:2605.24660, 2026). Position matters too — retrieval accuracy depends
on *where* in the context the relevant item sits (Liu et al., TACL 2023).

**(f) Mapping to SAEA.** This is the owner's principle (2), and the base is built for it: six nodes,
each one config key with an OFF null arm, sealed one-factor cells, own-null margins, derangement
twins. SAEA should *not* adopt AFlow/ADAS open-ended search — the cost model (GPU-hours per candidate,
one experiment in flight) forbids it, and open-ended code generation contradicts the
one-base/thin-derivations rule. It should adopt the **ablation reading**: the existing OFF arms already
produce a node × (quality, prefill tokens, GPU-h) table whose Pareto frontier is free. Two published
results predict SAEA findings directly — B7a (-0.31 SLU for +11.6% GPU-h) is a node off the frontier,
and EFF-1 (the Solver seeing the Reviewer's tools) is the LongFuncEval effect, a tool-catalogue
contamination rather than a prompt bug. The index losing 7.4 pp is also readable as "lost in the
middle": an index buried in a long constant prefix sits in the worst position for retrieval.

---

## 7. Evolutionary and Pareto methods for cost–quality

**(a)** Quality and cost are two objectives, and the right object is a frontier, not a point.
FrugalGPT names the three levers — prompt adaptation, LLM approximation, LLM cascade — and reports
matching the best single model "with up to 98% cost reduction", or +4% accuracy at equal cost (Chen et
al., arXiv:2305.05176, 2023).

**(b)** Optimised: which path or model handles which row — routing, cascade order, early exit, per-row
budget.

**(c)** A cascade needs a confidence or verifier score to decide escalation and a labelled set to
calibrate it. RouteLLM learns routers from human preference data plus augmentation, reporting over 2x
cost reduction without quality loss and transfer when the strong/weak models are swapped (Ong et al.,
arXiv:2406.18665, 2024).

**(d)** Threshold cascades with a learned scorer; classifier-based routing; multi-objective/Pareto
selection — GEPA's frontier over candidate prompts is the prompt-space instance of the same idea.

**(e)** Router calibration is the whole method: a miscalibrated threshold either spends everything or
drops quality silently. Non-monotonicity (Chen 2024) says a fixed budget is generally wrong. Cascades
also break paired comparison — two rows answered by different paths are not exchangeable.

**(f) Mapping to SAEA.** One frozen core means model routing is out of scope, but *path* routing is
not. The base's cost units (prefilled tokens/row, GPU-h/1,080 rows) plus per-stratum tables already
form a two-objective record; nothing prevents plotting the admitted-module set as a frontier and
reporting the knee rather than the maximum. The concrete cell: a **cheap-path/expensive-path cascade**
where the expensive path (Reviewer x3 + Acquisition + long knowledge prefix) is entered only when the
Perception node's candidate-intent set is ambiguous, with the threshold calibrated on the construction
pool. Audit caution: routed arms must still be scored on the *full* manifest through
`core.scoring_batch`, never per path, or the comparison is no longer paired.

---

## 8. Synthesis

| Family | What is updated | How feedback is obtained | Gold labels? | Per-state or global | Typical cost |
|---|---|---|---|---|---|
| 1. Experience library | Persistent text store | Scalar score + NL contrast over a rollout group | Mixed: TF-GRPO/ExpeL yes (tens of items); DC/ACE no (execution feedback) | Global store, per-state retrieval | 10s–100s of rollouts; permanent prefill |
| 2. Prompt optimisation | Instruction strings, few-shot sets | Dev-set metric; GEPA also reads traces | Yes (dev set) | Global | GEPA 10s of rollouts; EvoPrompt/Promptbreeder 1000s |
| 3. Demonstration / retrieval policy | Retriever, k, ordering, retrieval depth | LM likelihood of gold, task reward, or bandit score | Yes to fit the selector; none at inference | Per-state (per row) | One retriever fit, or a fixed BAI budget |
| 4. Test-time search | Sample count, tree, revisions, decoding | Verifier / PRM / self-consistency | Verifier training yes; self-consistency no; Math-Shepherd auto-labels | Per-state (compute-optimal per prompt) | Linear in N per row, forever |
| 5. In-context RL | The context as learning history | Environment reward | No gold, but AD needs pretraining on histories | Per-episode | Not reachable for a frozen third-party core |
| 6. Structure search | Node set, control flow, tool set | Benchmark metric + execution feedback | Yes | Global | One full eval per candidate graph — most expensive family |
| 7. Cost–quality routing | Which path/model per row | Confidence / verifier score | Yes, for calibration | Per-state | One calibration set; saves at inference |

Two axes summarise it. **Label dependence**: families 1 (ACE/DC variant), 4 (self-consistency) and 5
run on unlabelled rollouts; 2, 3, 6 and 7 need a labelled search set. **Persistence of cost**: 1, 2
and 6 pay optimisation cost once and inference cost forever as prefill; 4 and 7 pay per row, every
row, for ever.

**The three principles most applicable to the SAEA base**, in order:

1. **Semantic advantage over a scored rollout group with an additive store update** (family 1, plus
   GEPA's reflect-on-the-trace). SAEA has the rollouts, the official scorer, the sealed traces and the
   gold-legal construction pool; it lacks only the operator turning a score-ordered rollout pair into a
   store delta. Additive deltas with per-item provenance preserve the one-factor-cell and OFF-null
   discipline that a wholesale view rewrite destroys, and are the documented defence against the
   brevity bias / context collapse the -7.4 pp index result resembles.
2. **Pareto-frontier reading over the existing OFF-null ablation table** (families 6 and 7). Costs
   nothing new: every admitted and rejected module already has a quality delta, a prefill-token cost
   and a GPU-h cost. Reporting the frontier rather than the argmax makes results like B7a decidable
   without a new flight — and GEPA's evidence says keeping the per-stratum frontier, not the best
   average, is also the better *search* strategy.
3. **Budget as a tuned per-state parameter, with the verifier measured first** (family 4). Coverage
   scales but selection plateaus (Brown 2024) and voting is non-monotone in N (Chen 2024); SAEA's
   rejected logprob probe is the same ceiling seen locally. Before spending more on grouped Solver
   sampling or Reviewer x3, measure that verifier's selection precision against the official scorer on
   the construction pool, then pick N per stratum.

**Sources I could not verify, and therefore did not lean on.** I opened only the abstract of
Training-Free GRPO, so no rollout-group size is claimed above. I could not confirm from a primary page
the journal version of TextGrad, the NeurIPS/ICLR venues of Reflexion, DSPy, Voyager, AFlow and ADAS,
or venues for Agent Workflow Memory and Math-Shepherd — these are cited by arXiv id and year only.
Dynamic Cheatsheet's two variants (cumulative vs retrieval-and-synthesis) appear in secondary
descriptions but not on the page I opened, so I did not describe them. The LongFuncEval abstract page
would not load; I read the arXiv HTML version instead. The Repantis 2026 tool-shortlist result rests
on a single abstract page and should be re-read before any submission use.

---

## References

All entries were opened at an arXiv abstract/HTML page or a publisher page on 2026-09-21.

1. Cai, Yuzheng, et al. *Training-Free Group Relative Policy Optimization.* arXiv:2510.08191, 2025.
2. Shinn, Noah, et al. *Reflexion: Language Agents with Verbal Reinforcement Learning.* arXiv:2303.11366, 2023.
3. Zhao, Andrew, et al. *ExpeL: LLM Agents Are Experiential Learners.* AAAI-24, 38(17):19632–19642, 2024; arXiv:2308.10144.
4. Suzgun, Mirac, et al. *Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory.* arXiv:2504.07952, 2025.
5. Wang, Guanzhi, et al. *Voyager: An Open-Ended Embodied Agent with Large Language Models.* arXiv:2305.16291, 2023.
6. Wang, Zora Zhiruo, et al. *Agent Workflow Memory.* arXiv:2409.07429, 2024.
7. Zhang, Qizheng, et al. *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models.* arXiv:2510.04618, 2025.
8. Yang, Chengrun, et al. *Large Language Models as Optimizers* (OPRO). arXiv:2309.03409, 2023.
9. Yuksekgonul, Mert, et al. *TextGrad: Automatic "Differentiation" via Text.* arXiv:2406.07496, 2024.
10. Pryzant, Reid, et al. *Automatic Prompt Optimization with "Gradient Descent" and Beam Search.* EMNLP 2023; arXiv:2305.03495.
11. Fernando, Chrisantha, et al. *Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution.* arXiv:2309.16797, 2023.
12. Guo, Qingyan, et al. *EvoPrompt: Connecting LLMs with Evolutionary Algorithms Yields Powerful Prompt Optimizers.* ICLR 2024; arXiv:2309.08532.
13. Agrawal, Lakshya A., et al. *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning.* ICLR 2026 (Oral); arXiv:2507.19457.
14. Opsahl-Ong, Krista, et al. *Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs* (MIPRO). EMNLP 2024; arXiv:2406.11695.
15. Khattab, Omar, et al. *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines.* arXiv:2310.03714, 2023.
16. Liu, Jiachang, et al. *What Makes Good In-Context Examples for GPT-3?* (KATE). arXiv:2101.06804, 2021.
17. Rubin, Ohad, et al. *Learning To Retrieve Prompts for In-Context Learning* (EPR). NAACL-HLT 2022; arXiv:2112.08633.
18. Zhang, Yiming, Shi Feng and Chenhao Tan. *Active Example Selection for In-Context Learning.* EMNLP 2022, aclanthology 2022.emnlp-main.622.
19. Shi, Chengshuai, et al. *Efficient Prompt Optimization Through the Lens of Best Arm Identification* (TRIPLE). NeurIPS 2024; arXiv:2402.09723.
20. Jeong, Soyeong, et al. *Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity.* NAACL 2024, aclanthology 2024.naacl-long.389.
21. Wang, Xuezhi, et al. *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* ICLR 2023; arXiv:2203.11171.
22. Cobbe, Karl, et al. *Training Verifiers to Solve Math Word Problems.* arXiv:2110.14168, 2021.
23. Lightman, Hunter, et al. *Let's Verify Step by Step.* arXiv:2305.20050, 2023.
24. Wang, Peiyi, et al. *Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations.* arXiv:2312.08935, 2023.
25. Yao, Shunyu, et al. *Tree of Thoughts: Deliberate Problem Solving with Large Language Models.* NeurIPS 2023; arXiv:2305.10601.
26. Zhou, Andy, et al. *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models* (LATS). ICML 2024; arXiv:2310.04406.
27. Snell, Charlie, et al. *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters.* arXiv:2408.03314, 2024.
28. Brown, Bradley, et al. *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling.* arXiv:2407.21787, 2024.
29. Chen, Lingjiao, et al. *Are More LLM Calls All You Need? Towards Scaling Laws of Compound Inference Systems.* arXiv:2403.02419, 2024.
30. Deng, Haikang, and Colin Raffel. *Reward-Augmented Decoding: Efficient Controlled Text Generation With a Unidirectional Reward Model.* EMNLP 2023; arXiv:2310.09520.
31. Mudgal, Sidharth, et al. *Controlled Decoding from Language Models.* ICML 2024; arXiv:2310.17022.
32. Khanov, Maxim, et al. *ARGS: Alignment as Reward-Guided Search.* ICLR 2024; arXiv:2402.01694.
33. Laskin, Michael, et al. *In-context Reinforcement Learning with Algorithm Distillation.* arXiv:2210.14215, 2022.
34. Brooks, Ethan, et al. *Large Language Models can Implement Policy Iteration* (In-Context Policy Iteration). arXiv:2210.03821, 2022; NeurIPS 2023.
35. Zhang, Jiayi, et al. *AFlow: Automating Agentic Workflow Generation.* arXiv:2410.10762, 2024.
36. Hu, Shengran, et al. *Automated Design of Agentic Systems* (ADAS). arXiv:2408.08435, 2024.
37. Kate, Kiran, et al. *LongFuncEval: Measuring the Effectiveness of Long Context Models for Function Calling.* arXiv:2505.10570, 2025.
38. Repantis, Vyzantinos, et al. *How Many Tools Should an LLM Agent See? A Chance-Corrected Answer.* arXiv:2605.24660, 2026.
39. Liu, Nelson F., et al. *Lost in the Middle: How Language Models Use Long Contexts.* TACL 2023; arXiv:2307.03172.
40. Madaan, Aman, et al. *Self-Refine: Iterative Refinement with Self-Feedback.* arXiv:2303.17651, 2023.
41. Huang, Jie, et al. *Large Language Models Cannot Self-Correct Reasoning Yet.* ICLR 2024; arXiv:2310.01798.
42. Chen, Lingjiao, et al. *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance.* arXiv:2305.05176, 2023.
43. Ong, Isaac, et al. *RouteLLM: Learning to Route LLMs with Preference Data.* arXiv:2406.18665, 2024.
44. Qin, Yujia, et al. *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.* arXiv:2307.16789, 2023.
