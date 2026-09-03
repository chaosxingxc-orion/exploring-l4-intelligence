# Owner amendment — semantic AgentLoop engineering baseline (2026-09-03)

This record translates the owner's 2026-09-03 instructions in substance. It amends the bounded
Audio2Tool carrier admission in the 2026-08-15 dual-track record and the experiment-ordering
language in later readiness notes. It does not alter the frozen-core boundary, open test data,
authorize Stage-3 work, or establish an effectiveness claim.

## Authorized Stage-2 sequence

Proceed now with bounded research on an engineering baseline built with OpenJiuwen AgentLoop and
the API-shaped frozen Qwen3-Omni core. Analyze the construction/training corpus as a population,
including its task structure, information requirements, label and difficulty distributions, and
retrieval reachability. Do not substitute an anecdotal handful of samples for that analysis.

The first scored successor must use at least 100 discovery examples. It must compare a direct
single-call baseline, a matched AgentLoop treatment, and a content-matched negative control that
breaks the relationship between a recipient observation and its supplied evidence. Keep gold,
reference transcripts, scorer output, test annotations, and future turns outside runtime. Analyze
OBS, ORG, SUPPLY, and USE separately, and report both end-to-end task effects and causal evidence
gain.

The engineering baseline is not required to exceed 0.90. The greater-than-0.90 objective applies
after the later training-free policy contribution. Scale to approximately 1,000 discovery examples
only after the at-least-100 experiment shows a stable paired gain, and require a new preregistration
before that scale step. Larger confirmation and test use remain closed.

## Knowledge construction and consumption

Treat knowledge construction and knowledge consumption as distinct stages. First determine which
information is necessary to reduce the model's decision from the full task action space to an
auditable top-K set and which information supports argument binding and ordered multi-action
execution. Then test whether the frozen core can consume that selected information.

Define reachability with explicit post-seal upper bounds rather than by handing the model a large
redundant corpus. At minimum report gold-tool coverage in top-K, complete ordered-call-skeleton
coverage, proposal-content coverage, and the action-set consumption ceiling. If knowledge
consumption fails while those upper bounds are high, improve decision cards or evidence-use
procedure on a new discovery cohort. If the upper bounds are low, return to knowledge construction
and expand or reorganize the knowledge source. Do not tune on the failed cohort.

## Retriever and frozen-core roles

Use the pinned local Qwen3 semantic embedding model as a frozen tool-level retriever when it wins a
construction-corpus, out-of-fold comparison against lexical retrieval. It may reduce the 152-tool
space to a sample-specific candidate set, but it is not an answering model and receives no runtime
gold. The frozen speech-capable core remains the only model allowed to interpret speech into a
label-free observation state and to author the final answer. Compare transcript-derived,
model-produced intent-query, and fused retrieval after sealing so their marginal information can be
measured.

## Runtime and evaluation efficiency

Do not estimate a loop's context from step count. Immediately before each model contact, serialize
the exact current transport request and measure it with the pinned service tokenizer. The present
32,768-token per-slot service limit is a physical deployment limit, not a target; retain at least
8,192 tokens of operational reserve. A later loop step may proceed only if its own measured request
fits.

Sample-level concurrent execution remains allowed. Use the established two-slot, queue-depth-four
generation geometry until a separate throughput study changes it. Batch the local embedding inputs
where the pinned server supports it; do not combine multiple task examples inside one generation
prompt. Run the unchanged official scorer as one single-process job per complete manifest, and use
an outer coordinator to run independent complete-manifest jobs in parallel. Never shard a manifest
and average shard scores. Network jitter is not an engineering-baseline variable.

## Training-free policy space

Leave the control-policy boundary open while building the baseline. Reuse a pinned open-source
implementation rather than implementing a repository-specific learner. The current primary asset
is Vowpal Wabbit 9.11.2 `cb_explore_adf`; the answering core stays parameter-frozen. Collect only
deployment-visible context, complete action identities, propensities, and post-seal rewards on
discovery data. A policy contribution is established only by an out-of-fold or disjoint-validation
gain over both direct single-call and fixed AgentLoop baselines.

Every model or tool contact still requires a structured ExecutionPlan, exact split and protocol
hashes, a pre-registered exposure row, and one-shot accounting before its result is read.
