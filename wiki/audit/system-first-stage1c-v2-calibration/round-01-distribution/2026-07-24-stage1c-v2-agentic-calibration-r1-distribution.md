---
title: "Stage-1C v2 Agentic calibration R1 distribution"
date: "2026-07-24"
artifact_type: "CALIBRATION_DISTRIBUTION_TRANSACTION"
campaign: "system-first-stage1c-v2-calibration"
round: "round-01-distribution"
method_contract_commit: "ee12a3a79bd578df996c44c4bdb2dbc709e2f616"
accept_verdict: "ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE"
coder_distributed: true
both_raw_outputs_frozen: false
agreement_computed: false
push_authorized: false
---

# Calibration distribution transaction

After the exact RC2R3 independent ACCEPT was registered, two fresh no-fork coder contexts were bound:

- A: `gpt-5.6-sol`, `/root/stage1c_coder_a_r1`, transaction
  `STAGE1C-RC2R3-TX-A-R1`;
- B: `gpt-5.6-terra`, `/root/stage1c_coder_b_r1`, transaction
  `STAGE1C-RC2R3-TX-B-R1`.

Each received eight artifacts extracted from the accepted commit into a separate no-`.git` workspace.
Receiver-side raw-byte recomputation yielded the same bundle
`03674710223ad3c457e6568bdc83b66c1491abd84dd4e6d2c16495065e3ead64` and prompt
`88fca5a601bc49b946e2c29fcac35ba212dec38af5625c312a964535201aaa8e`.
The 135 source renditions were copied to a shared isolated source root and all source-manifest lengths
and SHA-256 values were reverified.

Delivery receipt hashes are:

- A: `631747d9f61f67c32f0b1f9e7081abc053dc1bcf3ae609a9338054ab40c67bf3`;
- B: `228767d27211017f19cdb241c0ca2de2cdf00fa3414be4a80b5b0046d9403680`.

The coders may read only their eight-file input, their receipt and the shared frozen source bytes.
They may not inspect the repository, network discovery, prior labels/readiness or the other coder's
output. This records two isolated model coders, not provider-independent or human inter-rater
independence.

Both raw N=56 outputs remain pending. Agreement is prohibited until both are complete, schema-valid
and frozen. Owner adjudication, calibration release review, mapping signature, research execution,
Stage-2A and push remain closed.
