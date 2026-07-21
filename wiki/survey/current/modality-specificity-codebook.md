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

## Calibration examples before Stage-1B execution

These rows are calibration exercises, not final paper codings and not occupancy evidence. Their purpose
is to expose ambiguous fields before systematic execution. They must be dual-coded again from frozen
full text before any value becomes load-bearing.

| Paper | Calibration role | Provisional seven-field pattern | Known ambiguity / expected disagreement |
|---|---|---|---|
| AudioToolAgent (`2510.02995`) | speech/omni tool-agent positive calibration | `audio_native_single`; remaining six fields initially `UNKNOWN` until D2 | whether tools only read task-provided audio or inject new information; whether action timing is post-utterance or inter-turn |
| Thinking While Listening (`2509.19676`) | audio test-time-scaling boundary calibration | `audio_native_single`; `offline_batch`; `whole_clip`; other fields `UNKNOWN` until D2 | whether the relevant evidence path consumes raw waveform or a learned representation and whether any state persists across samples |
| OmniAgent / Native Active Perception (`2606.19341`) | native omni sequential-control calibration | `omni_native_joint`; `mixed`; remaining fields `UNKNOWN` until D2 | observation granularity, persistent textual memory, on-demand perception timing, and trained-system boundary must be resolved separately |

The calibration acceptance condition is three completed dual-coded rows with a field-level agreement
report and adjudication of every disagreement. Until then, H5 remains a mapping hypothesis rather than a
finding.

