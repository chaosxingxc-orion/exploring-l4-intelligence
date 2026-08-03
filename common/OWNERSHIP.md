# speechrl-common module ownership audit

First audit recorded 2026-08-03 under the post-reorganization remediation
(`PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1`, P2-1). The library predates the W1–W4 retirement;
this page states, per module, who actually consumes it today and what its lifecycle status is.

Status vocabulary:

- `PROGRAM_INFRA_CANDIDATE` — genuinely program-level utility, retained in the active API surface,
  but **no admitted study consumes it yet**; it becomes `SHARED` only after at least two admitted
  studies consume it through a pinned dependency.
- `LEGACY_W_ERA` — only the retired W1–W4 works ever consumed it. Kept for provenance and possible
  future adoption; excluded from the active API story; a new consumer must adopt it explicitly
  (study migration-manifest row + umbrella commit pin), not inherit it.

Consumer rule: as of 2026-08-03 the admitted study `audio-aware-evidence-acquisition` does **not**
import `speechrl_common` (its migration manifest defers the dependency until first consumption, with
an exact-commit pin required at that point). Active consumers of every module: **none** — the only
runtime consumer of this package today is its own test suite (`common/tests`).

| Module | Status | Historical consumer | Owner | Notes |
|---|---|---|---|---|
| `audio/io` | PROGRAM_INFRA_CANDIDATE | W1/W4 | umbrella | audio load/resample |
| `audio/features` | PROGRAM_INFRA_CANDIDATE | W1/W4 | umbrella | log-mel features |
| `data/registry` | PROGRAM_INFRA_CANDIDATE | W1–W4 | umbrella | dataset registry + data-root resolution |
| `tracking/mlflow_logger` | PROGRAM_INFRA_CANDIDATE | W1/W4 | umbrella | local-MLflow run helper |
| `utils/seed`, `utils/logging`, `utils/checkpoint` | PROGRAM_INFRA_CANDIDATE | W1–W4 | umbrella | determinism/log/path helpers |
| `rl/reward` | PROGRAM_INFRA_CANDIDATE | W1 | umbrella | WER/ASR/exact-match verifiable rewards |
| `rl/metrics` | PROGRAM_INFRA_CANDIDATE | W1/W3 | umbrella | accuracy/F1/BLEU/chrF/EER |
| `rl/decode` | LEGACY_W_ERA | W1 | umbrella | decode utilities |
| `rl/embedding_metrics` | LEGACY_W_ERA | W4 | umbrella | recall@k/MRR/retrieval |
| `rl/probe` | LEGACY_W_ERA | W4 | umbrella | linear/kNN probe accuracy |
| `rl/disentanglement` | LEGACY_W_ERA | W4 | umbrella | separation/silhouette/leakage (dead flagship) |
| `eval/probing` | LEGACY_W_ERA | W4 | umbrella | probing/retrieval harness over frozen embedder |
| `models/qwen2_audio` | LEGACY_W_ERA | W1 | umbrella | HF speech-LLM loader |
| `models/generative_omni` | LEGACY_W_ERA | W1 | umbrella | generative omni loader |
| `models/omni_embed` | LEGACY_W_ERA | W4 | umbrella | sentence-transformers omni-embed backbone |
| `models/prompts` | LEGACY_W_ERA | W1 | umbrella | prompt templates |
| `configs/base.yaml` | LEGACY_W_ERA | W1–W4 | umbrella | Hydra base the retired works composed on |

Deprecation posture: nothing is deleted in this audit. `LEGACY_W_ERA` modules stay importable so
history and tests keep passing, but they must not be presented as the shared capability surface of
new studies. Physical removal or extraction decisions are deferred to the post-R0 module-shrink pass
(remediation transaction T5 timing rule); any removal follows the umbrella archive discipline.
