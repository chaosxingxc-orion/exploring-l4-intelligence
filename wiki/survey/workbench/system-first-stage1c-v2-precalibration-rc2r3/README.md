# Stage-1C v2 Agentic RC2R3 runtime-integrity contract

Status: `AGENTIC_RC2R3_CODER_READY_NOT_DISTRIBUTED`.

RC2R3 is an immutable successor to committed RC2R2. It changes exactly three runtime-integrity
properties identified by the commit-bound RC2R2 review:

1. every agreement critical gate uses the compiled constant `0.85`; callers cannot lower or replace
   it;
2. delivery receipts are constructed from the receiver's actual artifact and prompt `bytes`, with an
   exact eight-artifact set, per-file length/SHA256 and bundle digest recomputed before a receipt is
   emitted;
3. leakage allowlists use typed key/index path segments. Display strings use escaped JSON-pointer
   notation only after authorization decisions, so literal keys cannot impersonate array positions.

The coder-visible semantic content is inherited from RC2R2 except the agreement contract, which now
states the frozen threshold and actual-byte/typed-path rules. The N=56 identity set, response schema,
source bytes, blank packet, codebook and prompt remain unchanged. Specialized Duplex remains an
exclusion boundary.

No coder has received the package. No agreement, adjudication, mapping, research-model call,
benchmark metric, paper reproduction, prototype, novelty verdict or push is recorded. Distribution
requires the exact fresh-review verdict
`ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE`.

Machine entrypoints:

- builder/checker: `scripts/survey/sf_stage1c_v2_precalibration_rc2r3.py`;
- agreement engine: `scripts/survey/sf_stage1c_v2_calibration_agreement_v5.py`;
- adversarial tests: `scripts/survey/test_sf_stage1c_v2_precalibration_rc2r3.py`;
- exact review manifest: `review-package-manifest-rc2r3.json`.
