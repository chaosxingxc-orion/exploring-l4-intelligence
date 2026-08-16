# Speech-aware evidence acquisition: Stage-2A engineering entry contract

## Status

Stage-1C received `PASS_STAGE1C_FORMAL_OPENING` on 2026-08-02, the owner issued GO on 2026-08-03, and on
2026-08-04 the object was narrowed to speech-only and the semantic identity migration was completed. The
authoritative frozen values are those in
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`;
this document specifies the E0→R0→R1→X engineering order.

```yaml
semantic_research_object: speech-aware evidence acquisition
source_candidate_provenance: R2
stage1c_decision: PASS_STAGE1C_FORMAL_OPENING
authorization: OWNER_GO_AND_EXECUTION_CONTRACT
authorization_record: wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md
domain: speech-only
general_audio: excluded_from_study_but_retained_locally
novelty_status: NOT_YET_DETERMINED
method_status: EXPLORATION_SPACE_ONLY
repository_slug: speech-aware-evidence-acquisition
repository_url: https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git
experiment_index: wiki/experiments/speech-aware-evidence-acquisition/README.md
```

## Purpose

Stage-2A's primary task is not to keep expanding the paper and data lists, but to turn the research
question into executable, attributable, re-verifiable speech-domain experiments. First prove that carrier
identity, the information boundary, the scorer, the trace and the closest-prior path are runnable; only
then test candidate mechanisms of the external control plane. Novelty and the final technical method are
still decided by Stage-2A/2B evidence.

## Immutable boundary

- The frozen Qwen3-Omni core is reached only across an API-shaped boundary; parameters, structure and the
  acoustic training paradigm are never modified.
- No task-trained model, and no second LLM holding final answer authority.
- Scope covers only the speech signal and language tasks; general/environmental audio data must never
  enter any arm.
- Gold answers, reference transcripts, test annotations and future turns must never enter runtime.
- `OBS`, `ORG`, `SUPPLY` and `USE` are traced separately; external responses, tool actions, requests and
  derivatives are all versionable and hashable.
- Discovery and confirmatory stay isolated; confirmatory rules are frozen before any result is read.

## Research axes

1. `OBS`: transcripts, entities and segment observations formed from the speech signal;
2. `ORG`: the granularity, structure, indexing, provenance and temporal organization of knowledge;
3. `SUPPLY`: evidence selection, quantity, ordering, templates and supply timing;
4. `USE`: evidence admission, verification, rejection, re-querying, stopping and final adoption.

A single mechanism experiment may treat only the pre-registered axis as the intervention; every other axis
must be frozen or included in a full factorial. Reporting only the "total score before and after adding
knowledge" cannot support a mechanism conclusion.

## Entry sequence

### E0 — model-free closure

1. Establish cross-layer sample/segment identity for `earnings21-original`, `earnings22-original` and `conec`;
2. Fix the runtime visible fields and leakage checks for each arm;
3. Fix the WER/entity/QA scorer, normalization, correct-to-wrong and wrong-to-correct;
4. Produce ten-sample loader/provenance/four-axis trace receipts;
5. Verify license/redistribution, with dataset identity referenced only from `docs/datasets.lock.json`;
6. Explicitly check that FSD50K, AudioSet and ESC-50 have not entered the dependency graph or the test
   discovery path.

### R0 — reproduction-zero vertical slice

- One discovery carrier and one unread confirmatory carrier;
- Deterministic loader, frozen-core adapter, four-axis trace and scorer adapters;
- Three engineering controls: bare core, fixed legal context, and fixed retrieval/context;
- A random/mismatched-evidence negative control and an oracle-evidence upper-bound interface (the oracle
  never enters formal runtime);
- URI/hash linkage between MLflow and the umbrella experiment index;
- Accounting of calls, tokens, latency, GPU/CPU, speech-audio seconds and evidence bytes.

R0 verifies wiring and measurement integrity only; it constitutes no evidence of superiority or novelty.

### R1 — closest/strongest-prior reproduction

Prioritize freezing the ConEC/contextual ASR, RECOVER-style correction, entity resolution and
contextual-biasing candidates under the same speech task, carrier and information boundary. Before the
first run, record the exact runnable revision, prompt, scorer and any reason a candidate cannot run. If a
frozen mandatory baseline fails, report `INCONCLUSIVE_BASELINE_NOT_READY`.

### X — directional exploration

After at least one credible closest-prior reproduction, test in order of minimum distinguishability:

1. Whether `OBS` reduces entity mishearing;
2. With OBS frozen, whether `ORG/SUPPLY` improves legal-evidence accessibility;
3. With supply frozen, whether `USE` reduces correct-to-wrong caused by incorrect evidence;
4. Whether a reward-guided next action beats a fixed single retrieval / fixed rerank;
5. Whether the gain is retained on secondary speech carriers rather than only fitting Earnings.

## Evaluation gates

| Gate | Must answer |
|---|---|
| Effectiveness | Do the task/entity/QA metrics improve, and are the distribution and the tail stable? |
| Reasonableness | Which axis does the gain come from? Is the evidence relevant, sourced and free of gold leakage? Does it increase correct-to-wrong? |
| Efficiency | How many calls, tokens, latency, GPU/CPU, speech seconds and evidence bytes does the gain cost? Is it on the Pareto frontier? |

## First two-week deliverable

- The four E0 gates and the runtime receipt;
- An end-to-end discovery/confirmatory path for the core carrier;
- The bare/fixed-context/random-evidence/oracle-bound controls;
- One readiness-qualified closest-prior smoke/reproduction attempt;
- One joint effectiveness/reasonableness/efficiency table;
- A go/narrow/repair/stop memo for the next slice.

Stop the line immediately on information leakage, sample-identity drift, scorer inconsistency, licensing
problems, a non-reproducible runtime pin, or an unaddressed stronger runnable prior at the same boundary.

## Literature and data delta policy

Literature is adopted through a bounded weekly delta lane. New work by default only updates the
prior/threat queue; Stage-1 reopens only when the research question, carrier legality, information
boundary or reproducibility contract is overturned. A dataset mentioned in a new paper creates no
download obligation automatically; it enters an acquisition proposal only when it is consumed by a
pre-registered experiment, baseline or diagnostic question, and is under 1 TB, publicly available and
acceptably licensed.
