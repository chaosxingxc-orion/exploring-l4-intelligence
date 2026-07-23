---
artifact_id: "SF-STAGE1C-COMMON-RUBRIC-COMPARISON-V1"
owner_stage: "STAGE_1C"
ordering: "UNRANKED"
selection_status: "NOT_SELECTED"
execution_authority: "WITHHELD"
---

# Stage-1C common-rubric problem comparison

The independent v5 rereview signed `SIGN_STAGE1C_COMMON_RUBRIC_COMPARISON`. This table starts the
authorized evidence-only comparison. It does not rank the bundles, select a problem, establish
novelty, or authorize model/API calls, benchmark metrics, reproduction or prototypes. The
machine-readable authority, routes and assessments are in
`../data/stage1c-common-rubric-comparison-v1.json`.

## Comparison state

| bundle ID | problem family | state |
|---|---|---|
| `BUDGET_STOP_REPAIR` | budget / stopping / repair | `UNRANKED_NOT_SELECTED` |
| `EVALUATOR_REWARD_RELIABILITY` | evaluator / reward reliability | `UNRANKED_NOT_SELECTED` |
| `INTERACTIVE_FULL_DUPLEX_OBJECTIVES` | interactive / full-duplex objectives | `UNRANKED_NOT_SELECTED` |

## One common rubric

| rubric dimension | `BUDGET_STOP_REPAIR` | `EVALUATOR_REWARD_RELIABILITY` | `INTERACTIVE_FULL_DUPLEX_OBJECTIVES` |
|---|---|---|---|
| `problem_distinctness` | Distinct only as external continue/stop/retry/repair/rollback under evaluator noise and finite budget; generic stop/repair is occupied. | Distinct when an external proxy must drive decisions and no sufficient deterministic oracle exists; not a generic “audio judge missing” claim. | Distinct as the gap between task success and interaction quality under interruption, timing, recovery and tools; not generic voice naturalness. |
| `decision_causality` | A signal must change the next call, selected candidate, stop or repair action. MUGEN is consensus selection. | A judge becomes control evidence only when it changes selection, stop or repair; an instrument alone is not a controller. | A signal must change turn-taking, tool action, state update, recovery or timing; a benchmark alone is not a controller. |
| `measurement_validity` | Separate oracle headroom, realized gain, regret, harm and unnecessary calls from proxy acceptance. | Separate pointwise/pairwise/listwise/tie protocols, calibration and bias, human agreement and downstream utility. | Keep terminal success, tool correctness, interruption/recovery, latency and interaction quality as distinct axes. |
| `modality_necessity` | Audio is load-bearing only where acoustics, speaker state or timing changes the optimal action beyond transcripts. | TRACE, S2S-Arena and MTalk-Bench expose voice-quality, prosody, speaker and nonverbal information beyond transcripts. | Speech timing, prosody and nonverbal cues are load-bearing; audio-only and AV2AV claims remain stratified. |
| `failure_severity` | Early stop, wasted calls, rejected correct answers, harmful repair and cost/latency overruns. | Systematic mis-ranking, bias amplification, incorrect stopping and harmful repair. | Missed interruption, stale state, wrong tool action, unsafe recovery and superficially natural task failure. |
| `feasibility` | Relevant papers and local assets exist, but the exact Stage-2A task/evaluator/licence is not selected. | Several papers and repositories are local; exact unavailable/manual/terms-gated assets retain those states. | Several benchmarks are local or revision-pinned; some exact data remain unavailable, terms-gated or generator-only. |
| `reproduction_anchor` | Task-matched speech stop/repair prior, MUGEN consensus and VRR-Stop are candidates; none is frozen. | TRACE deterministic fusion and speech-native pairwise instruments are candidates; trained rewards remain boundaries. | VoiceAgentBench, Full-Duplex-Bench, Audio2Tool, IHBench, S2S-Arena and MTalk-Bench are candidates; none is selected. |
| `scope_compatibility` | External budget, selection and rollback fit frozen API-visible control; SimulU is model-internal boundary. | Prompted/frozen external evaluators fit; trained reward models and hidden internal scores are boundaries. | Frozen speech/omni APIs with observable environment state fit; hidden streaming-state dependencies may not. |
| `evidence_maturity` | Routed full text and mechanism coding only; no project reproduction or outcome. | Measurement-rich, including four newly routed local full texts; no project decision-utility result. | Direct systems, instruments and AV boundary exist; no simulator validation, reproduction or live-user result. |

Every cell remains uncertainty-bearing. The detailed JSON records the specific uncertainty separately
from each assessment; no aggregate score is computed because engineering ease, evidence quantity and
problem importance are not interchangeable.

## Stage-1C routing corrections

- Five reviewer-directed outside-union identities now use
  `REGISTER_REVIEWER_DIRECTED_CANONICAL_ID_NO_DUPLICATE_SEED`; each retains one existing canonical
  work and creates no second claim seed.
- `Inference-Time Scaling for Joint Audio-Video Generation` is
  `BOUNDARY / TRANSFER_BOUNDARY_DIRECT_CONTROL`: its adaptive reward aggregation changes selection,
  but joint AV generation is not strict speech-agent direct occupancy.
- MUGEN is `SELF_CONSISTENCY_CONSENSUS`, not an external evaluator/verifier signal. The historical v5
  `9/9/8/0` release count remains immutable provenance and is not treated as the only natural taxonomy.

## Bounded priority intake

| canonical work | current route | role | active comparison use |
|---|---|---|---|
| `CW-ACL-2026.findings-eacl.151` — TRACE / Hearing Between the Lines | `INCLUDE` | `MEASUREMENT_INSTRUMENT` | evaluator decomposition and deterministic proxy fusion |
| `CW-ACL-2026.acl-long.1615` — S2S-Arena | `INCLUDE` | `MEASUREMENT_INSTRUMENT` | speech-native paralinguistic pairwise measurement |
| `CW-ARXIV-2508.18240` — MTalk-Bench | `INCLUDE` | `MEASUREMENT_INSTRUMENT` | multi-turn arena/rubric comparison and judge-bias evidence |
| `CW-ARXIV-2603.16924` — SimulU | `BOUNDARY` | `MODEL_INTERNAL_BOUNDARY` | long-form S2S policy comparator; cross-attention violates black-box access |

All four official identities are verified and their PDFs are local under `SPEECHRL_DATA_DIR`; both
arXiv items also have local e-print sources. This is bounded reviewer-directed intake, not renewed
broad discovery and not literature-universe closure.

## Bundle-specific checks retained

- `BUDGET_STOP_REPAIR`: distinguish fixed K from adaptive budget and environment terminal state from
  heuristic, consensus, uncertainty or evaluator stopping; repair must change the next action.
- `EVALUATOR_REWARD_RELIABILITY`: distinguish transcript-only, audio-aware, self-judge, external
  frozen judge and trained reward; TRACE deterministic fusion and Joint AV adaptive aggregation are
  different proxy-composition boundaries.
- `INTERACTIVE_FULL_DUPLEX_OBJECTIVES`: keep task success and interaction quality as co-primary axes;
  distinguish audio-only from AV2AV and retain interruption, barge-in, state update, resume, latency
  and tool correctness separately.

## Next gate

Continue evidence-only comparison and form an unexecuted problem-selection dossier for the owner.
Problem ranking, owner selection, novelty convergence, model execution, benchmark metrics,
reproduction and prototypes remain withheld.
