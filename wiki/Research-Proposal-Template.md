# Research Proposal Template

> 🌐 **English** · 中文见 [[Research-Proposal-Template_CN]]
>
> A **portable, project-agnostic** *proposal + pre-registration* form for any empirical research
> study. Copy it into your project, fill every required field **before running the pilot**, and keep
> it as the study's pre-registered record. **Nothing here is tied to a specific repo, model, task, or
> team** — repo/domain-specific items appear only as clearly-marked *examples* you can replace. The
> bar is high on purpose; the form's job is to make that bar **enforceable and auditable** instead of
> dependent on the reader.

**How to use.** Copy this file → fill §0 front-matter → fill §1–§3 and §5(T)/§6 **before** any run →
run §4 → record §5(E)/§7 → apply the §8 verification gates throughout. A field you cannot yet fill is
a signal the study is **not ready to pass that gate**, not a field to skip.

> *Examples use a speech / training-free-RL study for concreteness; they are labelled "**e.g.**" and
> are meant to be replaced with your own domain.*

---

## Core requirements (gates)

1. **Survey + small-scale validation before scale.** No idea proceeds to large-scale work until it
   has been surveyed (§3) **and** validated on a small-scale dataset (§4).

2. **Reproducible AND valid + independently verified + code reviewed.** Every reported result must be
   (a) **fully reproducible** — with a Repro Manifest (§4) — **and** (b) **valid**: from a
   **held-out, pre-registered** evaluation, not merely reproducible (a reproducibly cherry-picked or
   leaked number is still wrong). Each result is **independently verified by a third party** (§4
   defines this) and its **code reviewed** against a claim-specific checklist (§4).

3. **Two-tier gate before large-scale experiments.** Before any large-scale run, a study must pass
   **both**:
   - **(T) Theory gate** — a justification of the method/operator's convergence / well-posedness /
     regret, **with assumptions stated**. A **written** proof suffices; reserve **machine-checked
     proof (e.g. Lean) for finitary theorems** (a no-regression gate, a monotonicity property, margin
     arithmetic, finite-argmax well-posedness). For a one-shot finite selector a one-line
     well-posedness note + the relevant bound is enough — do **not** force a "convergence" proof where
     convergence is undefined.
   - **(E) Effectiveness gate** — effectiveness is established **empirically, never proven**: a
     **pre-registered** criterion met on the small-scale pilot (e.g. paired Δ>0, bootstrap CI lower
     bound > 0, regression/cost within budget; fixed seed; eval reproduces train).
   - Both gates are **hard**; effectiveness is **measured, not theorem-proved**. *(This is the key
     correction to the common mistake of demanding a "proof of effectiveness": a method's convergence
     can be a theorem, but whether it helps on real data is an empirical claim that is tested and can
     be refuted — never proven.)*

---

## 0. Front-matter

Copy this block to the top of the instance and keep it current.

```
> project: <project / repo>  ·  study: <short id or title>  ·  owner: <name>  ·  date: YYYY-MM-DD
> status: planned | running | confirmed | refuted | scoped(narrowed)   ·  version: vX.Y
> companion docs (optional): links to your project's north-star / plan / decision log / experiment
>   index, if it keeps them
```

- **status** is a simple lifecycle: `planned → running → confirmed | refuted | scoped`.

---

## 1. Research Idea & Falsifiable Hypothesis

State the idea, *then* pin at least one claim a result could **refute** — before any pilot.

- **Motivation / direction** (free text): the problem, the viewpoint, what you hope to find or solve.
- **Primary hypothesis (falsifiable)**: ≥1 claim written as an **inequality on a NAMED, measurable
  metric** (defined so a specific outcome would refute it).
  - *e.g.* `metric(method) − metric(baseline) ≥ δ` on a held-out set; or `A_t(e_t) > A_t(e_{t'})`
    (task-conditioned separation).
- **Pre-committed thresholds**: minimum effect size **δ** and significance level **α** (e.g. p<0.05),
  fixed now.

---

## 2. Success / Kill / Pivot Criteria (pre-registered)

Fill **before** the pilot. Fixing the decision rule now is what prevents HARKing (authoring the
hypothesis after seeing the numbers).

- **Go threshold** (claim accepted): <number on the metric>.
- **Kill threshold** (claim refuted → drop): <number>.
- **Pivot zone** (inconclusive → reshape/scope): <range>.
- **Mode**: exploratory | confirmatory.
- **Negative-result commitment**: if the kill threshold is met, it is reported as a **negative result**
  (a valid outcome — §7), not silently reworked.

---

## 3. Survey & Positioning

Justify the direction's value **and adversarially challenge it**; identify baselines; state what is
actually new.

- **Value + challenge / refinement**: support the direction, then argue against it; refine/extend into
  a more valuable point, or confirm the current one and analyze in depth.
- **Baselines named**: baseline **model · method/algorithm · data**.
- **Novelty delta** (one sentence): name the **single closest** prior work and state what this study
  does that it does not.
- **Citation registry**: every cited claim resolves to a **real, resolvable source** (arXiv/DOI/URL)
  and is recorded per-claim; **AI-suggested citations are verified before use**.

---

## 4. Reproduced Results (Baseline + Method Pilot)

Reproduce prior numbers first, then pilot **your own** method — two activities, two pass criteria.
Produce evidence that is **valid**, not merely reproducible.

**Repro Manifest (required)** — attach all of:
- pinned **data** revision/fingerprint (*e.g.* a `datasets.lock.json`); **code revision** (git SHA);
  **exact environment** (frameworks + versions + hardware/accelerator); **fixed seed(s)**; a single
  copy-paste **`reproduce:`** command; the **experiment-tracker run ID** (*e.g.* MLflow / W&B).

**(a) Baseline Reproduction** — success = reproduce the prior/survey numbers **within a stated
tolerance band**; **eval == train metric within tolerance**. (If the baseline can't be reproduced, any
claimed Δ is unsound.)

**(b) Method Pilot** — success = the §1 falsifiable lift, with:
- **N seeds or bootstrap CIs + a paired significance test** (per-item Δ).
- **Locked test set touched once**; model/hyperparameter/seed **selected only on dev**.
- **Selection criterion ≠ reported metric** where they could collude (*e.g.* label oracle-reward
  results as *headroom*, not deployable).
- **Full sweep reported**, not just the argmax config; **re-score the actually-deployed artifact**,
  not a proxy.
- **Multiple-comparison handling** (Holm/Bonferroni/FDR) **when scanning many** configs.

**Independent third-party verification** — a logged **independent re-run by a different person _or_ an
independent agent**, from a **clean checkout** (never the author's warm session), landing within the
declared tolerance band; record **re-runner identity + date + numbers + run ID**.

**Code-review log** (kept distinct from the re-run) — reviewer + date + change-request link, against a
claim-specific checklist: (1) score/label is **ground-truth-derived, not self-graded** by the system
under test; (2) **no leakage**, selection on dev only; (3) seed/env pinned; (4) `reproduce:` actually
runs from a clean checkout.

---

## 5. Theory & Effectiveness Gate (two-tier)

Match the gate **type** to what is provable vs measurable (Core Requirement #3).

- **(T) Theory** — the method/operator's convergence / well-posedness / regret **where tractable**,
  **method-typed**: iterative/optimizer ⇒ convergence/regret argument; finite selector/one-shot ⇒
  well-posedness note + the relevant bound. **Written proof + cited assumptions** suffices;
  **machine-checked proof (e.g. Lean) only for finitary lemmas**.
- **Assumptions** — list them; mark those **"to verify empirically"** (*e.g.* a factor's presence /
  linear-accessibility / steerability conditions).
- **(E) Effectiveness** — the **pre-registered empirical** criterion on the locked pilot (paired Δ>0,
  bootstrap CI LB>0, regression/cost gates). **Never a theorem.**

---

## 6. Risks, Threats to Validity & Ethics

| Risk | Likelihood × Impact | Resolving gate or experiment |
|---|---|---|
| *(seed)* metric gaming / Goodhart |  |  |
| *(seed)* over-optimization / multiple-testing |  |  |
| *(seed)* proxy ≠ deployed artifact |  |  |
| *(seed)* leakage / test-set selection |  |  |

- **Controls & ablations**: name the **control** condition(s) distinguishing the claimed cause from
  confounds, and the **ablation(s)** toggling each degree of freedom, including **≥1 negative control**
  where the effect should **not** appear.
- **Ethics, licensing & data governance** (only what applies):
  1. per-dataset **license + permitted use**.
  2. **consent / provenance** and **PII / sensitive-attribute** handling — *e.g.* biometric
     (voiceprint/face), health, affect/emotion, protected characteristics.
  3. one-line **dual-use / misuse** note: who could be harmed, and the intended-use scope.

---

## 7. Decision & Outcome

Close the loop with a recorded verdict — **a well-run negative result is a valid, valued outcome.**

- **Result vs the pre-registered criterion** (§2): cleared go / landed in pivot / hit kill?
- **Verdict**: **go | pivot | kill**.
- **Scaling rationale & budget** (if go): **what is invariant** vs **what could break** when scaling
  (size confounds, ceilings, distribution shift); **compute/cost budget** + a **stopping rule**.
- **On-accept hooks**: record the verdict in your project's **decision log / experiment index**, update
  its **status board**, and publish to the **team's shared knowledge base**.

---

## 8. AI Tools & Verification

AI may do heavy lifting, so every AI output passes a **verification gate** before it is trusted — the
guard against hallucinated citations and fabricated numbers.

| Stage | AI role | Tooling (examples) | Verification gate |
|---|---|---|---|
| Survey §3 | synthesize + challenge | literature-survey / deep-research tools | every claim resolves to a real source; per-claim registry |
| Reproduce §4 | implement + run | coding + code-review tools | independent reproduction from pinned data + `reproduce:` |
| Theory §5(T) | draft the proof | formal-proof tool (e.g. Lean) for finitary lemmas | machine-checked (e.g. `lake build` sorry-free) or peer-checked written proof |
| Validation | adversarial multi-role review | multi-agent review | recorded panel sign-off (roles below) |

- **Suggested adversarial panel**: Statistician · Reproducibility auditor · Theory critic · Domain
  expert · **Anti-gaming / failure-mode red-teamer**.
- **Anti-hallucination rule**: cited claims must resolve to a real source; **AI-generated numbers and
  code are not accepted until independently reproduced** from pinned data + a `reproduce:` one-liner.
- **Memory protocol**: durable findings go to the team's **shared, persistent knowledge base**;
  **personal scratch notes stay personal** and never substitute for the shared record.

---

## Optional — wiring into a project knowledge base

*Skip this section entirely if you are using the template standalone.* This shows how **one** project
(this repo) wires the generic form into its own tooling — copy the pattern, swap in your own.

- **§0 companion docs** → `[[Project-Thesis]]` (north star), the work's plan & feasibility (*e.g.*
  `[[W4-Research-Plan]]`, `[[W4-Training-Free-RL-Feasibility]]`), `[[Decision-Log]]`,
  `[[Per-Work-Status]]`, `[[Validation-Experiment-Matrix]]`; `status` reuses the matrix lifecycle.
- **§4 lockfile / tracker** → `docs/datasets.lock.json`; local MLflow run IDs.
- **§7 on-accept** → append a dated `[[Decision-Log]]` entry, update `[[Per-Work-Status]]`, add the
  `[[Validation-Experiment-Matrix]]` row, publish via `scripts/wiki-sync.sh`.
- **§8 memory** → shared = the GitHub Wiki (sourced from `wiki/`); personal scratch = mem0 MCP, never
  a substitute for the Wiki. See `[[AI-Collaboration]]`.
