---
artifact_id: "SF-MODALITY-SPECIFICITY-CODEBOOK-V1-2026-07-21-01"
role: "current Stage-1B coding input for H5; calibration rows are non-load-bearing"
stage1b_execution_authorized: false
---

# Speech/omni specificity codebook

H5 is operational only through the following seven fields. Each method path receives one allowed value
per field plus field-bound evidence. `UNKNOWN` means the source does not resolve the value;
`NOT_APPLICABLE` means the construct genuinely does not apply and requires a reason. Neither value can
support a speech/omni-specific headline claim.

## Fields and allowed values

| Field | Allowed values |
|---|---|
| modality topology | `text_only`; `audio_native_single`; `audio_native_multi`; `omni_native_joint`; `asr_then_text`; `text_then_tts`; `multimodal_parallel`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| temporal regime | `offline_batch`; `turn_based`; `streaming_unidirectional`; `streaming_duplex`; `event_driven_async`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| observation granularity | `whole_clip`; `utterance`; `turn`; `segment_or_chunk`; `frame_or_audio_token`; `tool_or_environment_event`; `trajectory`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| acoustic evidence provenance | `raw_waveform`; `learned_audio_representation`; `task_provided_audio_tool_readout`; `transcript_only`; `metadata_only`; `external_new_audio`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| latency/action timing | `pre_inference`; `intra_utterance_online`; `post_utterance`; `inter_turn`; `post_trajectory`; `asynchronous`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| output/action modality | `text`; `speech`; `non_speech_audio`; `multimodal_content`; `tool_action`; `environment_action`; `composite`; `UNKNOWN`; `NOT_APPLICABLE` |
| state persistence | `stateless`; `within_utterance`; `within_turn`; `cross_turn_session`; `cross_session_external`; `environment_persistent`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |

## Coding and dual disagreement

Two coders independently assign all seven fields for every core speech/omni path and every H5
calibration path. They must cite the same frozen full-text identity but may use different locators.
Exact agreement is required. A dual disagreement is recorded field-by-field and sent to an independent
adjudicator; it is never averaged, majority-voted, or silently converted to `UNKNOWN`. If the source
itself is ambiguous after adjudication, the final value is `UNKNOWN` with the competing readings and
locators preserved. A true non-applicability uses `NOT_APPLICABLE` plus a construct-specific reason.

## Calibration before Stage-1B execution

The only current calibration state is
`wiki/survey/current/data/modality-specificity-calibration-v1.json`. It binds AudioToolAgent
(`2510.02995`), Thinking While Listening (`2509.19676`), and Native Active Perception
(`2606.19341`) to locally cached PDF/eprint hashes. Implementer coder A has completed all 21
paper-by-field assignments with page locators. Those values are deliberately non-load-bearing; in
particular, the full text makes AudioToolAgent's text-only core plus audio-tool readouts a useful test of
whether a coder mistakes system input modality for native core modality.

The calibration acceptance condition is exactly two independent 21-field passes, an exact field-level
agreement report with denominator 21, and independent adjudication of every disagreement. The second
blind pass has not occurred, so the artifact status is `PENDING_SECOND_INDEPENDENT_CODER` and H5 remains
a mapping hypothesis rather than a finding.
