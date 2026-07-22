# Secondary-screening contract v1

## Purpose and unit

The unit is one canonical arXiv PDF, not an e-print, prior ledger row, title, or method mention. The
contract separates continued evidence retention from eligibility for the experiment shortlist. An
execution exclusion never deletes or invalidates the Stage-1B registry role.

## Required accounting

1. Inventory every file below `survey-fulltext` and hash it.
2. Require exactly one PDF per canonical arXiv ID; duplicate identities fail closed.
3. Emit exactly one analysis row per PDF. Extraction failures and low-text PDFs remain explicit rows.
4. Join all four Stage-1B registry shards, but treat the registry as a metadata subset rather than the
   local-corpus denominator.
5. Bind page-marked extracted text and every generated ledger by SHA-256.

## Execution dispositions

| Disposition | Operational meaning |
|---|---|
| `EXCLUDE_MODEL_OPERABLE` | The paper's method explicitly trains/fine-tunes/optimizes a component or changes model internals/architecture. Keep as a comparator, not a TF-Strict execution candidate. |
| `EXCLUDE_MODEL_INTERNAL_ACCESS` | A load-bearing method signal requires hidden states, attention, logits/logprobs, activations, or equivalent internal visibility. |
| `EXCLUDE_VERTICAL_DATA_BARRIER` | The paper is vertical-domain work and its load-bearing data has explicit private/non-public/restricted evidence. |
| `BOUNDARY_OR_NEGATIVE_ONLY` | Stage-1B retained it as negative/boundary evidence; it cannot silently become an execution candidate. |
| `INSTRUMENT_ONLY` | Its primary role is benchmark, metric, dataset, or evaluation instrumentation. |
| `PRIORITY_DIRECT` | Frozen/black-box external control, speech/audio primary object, local task data, and a signal-to-action control path are all evidenced. |
| `TRANSFER_ONLY` | The external-control mechanism is relevant, but task/data fit is not direct enough for execution. |
| `MANUAL_REVIEW_ACCESS_AMBIGUOUS` | A control path exists but the access/training contract is not resolved. |
| `LOW_PRIORITY_NO_CONTROL_PATH` | No load-bearing reward/evaluation-to-action path was found in the deterministic pass. |

## False-positive controls

- Training requires first-person or proposed-method evidence; mentions in related work and baselines do
  not qualify.
- Agent/system architecture is not model architecture. Only encoder/decoder/adapter/Q-Former/prompt
  modifications count as model-operable evidence.
- POMDP/environment state is not a model hidden state. Internal access requires a decoder/encoder/model
  context or a direct internal-tensor operation.
- Short acronyms such as `ASR` and `TTS` use word boundaries; `AutoTTS` is not speech by substring.
- A vertical-domain term plus “no local match” is not proof that data is unobtainable. Only explicit
  restriction evidence supports `EXCLUDE_VERTICAL_DATA_BARRIER`.
- Registry `no_update_evidence` may resolve black-box compatibility, but cannot override contrary
  full-text training/internal-access evidence.

All automatic dispositions remain `DETERMINISTIC_SECONDARY_PREFILTER_REQUIRES_HUMAN_AUDIT`.
