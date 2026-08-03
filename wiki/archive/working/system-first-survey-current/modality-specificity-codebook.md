---
artifact_id: "SF-MODALITY-SPECIFICITY-CODEBOOK-V2-2026-07-21-01"
role: "current Stage-1B coding input for H5; calibration rows are non-load-bearing"
stage1b_execution_authorized: true
h5_load_bearing_use: "WITHHOLD_UNTIL_BLIND_CODER_B_AND_ADJUDICATION"
supersedes: "SF-MODALITY-SPECIFICITY-CODEBOOK-V1-2026-07-21-01"
---

# Speech/omni specificity codebook

H5 is operational only through the seven fields below. Every named method path receives one allowed
value per field plus field-bound evidence. The coding object is the executable path claimed by the
paper, not the paper title, benchmark, input dataset, or an imagined deployment.

## Analysis unit and level rule

- `modality_topology` describes the model that makes the path's central reasoning/control decision.
  External audio tools do not make a text-only controller audio-native.
- The other six fields describe the complete executable system path, including external tools,
  environment transitions, memory, and final output.
- Code the paper's primary evaluated path. Use `mixed` only when two or more allowed values are both
  essential on that same path. Ablations or separately evaluated variants receive separate method-path
  rows during Stage-1B; they are not collapsed into `mixed`.
- `UNKNOWN` means the frozen source does not decide between otherwise applicable values.
  `NOT_APPLICABLE` means the construct does not exist for that path and requires a reason.

## Fields and operational decisions

| Field | Operational decision | Allowed values |
|---|---|---|
| modality topology | Native modality of the central reasoning/control model. `audio_native_single` consumes audio in one native stream; `audio_native_multi` has multiple native audio streams/encoders; `omni_native_joint` jointly consumes audio plus at least one other native modality; `asr_then_text` and `text_then_tts` require that explicit cascade. | `text_only`; `audio_native_single`; `audio_native_multi`; `omni_native_joint`; `asr_then_text`; `text_then_tts`; `multimodal_parallel`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| temporal regime | Scheduling of observations and control. `turn_based` is a finite observation/action loop; streaming values require processing before the stream ends; `event_driven_async` requires events that can arrive independently of a fixed turn. | `offline_batch`; `turn_based`; `streaming_unidirectional`; `streaming_duplex`; `event_driven_async`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| observation granularity | Smallest evidence unit that can change the next system decision. Prefer the smallest explicitly actionable unit; do not infer frames/tokens from an encoder architecture alone. | `whole_clip`; `utterance`; `turn`; `segment_or_chunk`; `frame_or_audio_token`; `tool_or_environment_event`; `trajectory`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| acoustic evidence provenance | Acoustic information actually available to the executable path. `raw_waveform` includes raw media clips/spectrogram-equivalent model input; `learned_audio_representation` includes embeddings, logits, or category traces; `task_provided_audio_tool_readout` is an external tool's result about task-provided audio. | `raw_waveform`; `learned_audio_representation`; `task_provided_audio_tool_readout`; `transcript_only`; `metadata_only`; `external_new_audio`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| latency/action timing | Earliest point at which the coded action can affect the path. `post_utterance` acts only after the complete audio item; `inter_turn` acts between two or more control-loop turns; `post_trajectory` acts only after the complete rollout. | `pre_inference`; `intra_utterance_online`; `post_utterance`; `inter_turn`; `post_trajectory`; `asynchronous`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |
| output/action modality | What the path emits. `tool_action` is machine action without a content answer; `composite` requires both a tool/environment action and content/final answer on the same path. A textual or symbolic class label counts as `text`. | `text`; `speech`; `non_speech_audio`; `multimodal_content`; `tool_action`; `environment_action`; `composite`; `UNKNOWN`; `NOT_APPLICABLE` |
| state persistence | Longest boundary across which decision-relevant state survives. A control turn is one observation/action cycle: `within_turn` dies before the next cycle; `cross_turn_session` survives at least two cycles in one query/session; `cross_session_external` survives a new session. | `stateless`; `within_utterance`; `within_turn`; `cross_turn_session`; `cross_session_external`; `environment_persistent`; `mixed`; `UNKNOWN`; `NOT_APPLICABLE` |

## Tie-breaking precedence

1. Explicit method-path statements override architecture names, figures, benchmark descriptions, and
   author adjectives such as "real-time" or "omni".
2. For `post_utterance` versus `inter_turn`, choose `inter_turn` only when an action can alter a later
   control turn; otherwise a decision after full audio is `post_utterance`.
3. For `tool_action` versus `composite`, include the final answer in the same path. Tool call plus final
   answer is `composite`; tool call alone is `tool_action`.
4. For `raw_waveform` versus `learned_audio_representation`, code the representation delivered to the
   deciding component under the field's system-level rule. If both are independently decision-relevant,
   use `mixed` and cite both.
5. Prefer a resolved single value over `mixed`; prefer `UNKNOWN` over an unsupported inference; use
   `NOT_APPLICABLE` only when the field's construct is absent.

## Locator contract

Each assignment uses at least one `pdf_page` locator tied to the frozen PDF hash:

- `mode=exact_text_anchor`: `page` plus a human-readable phrase that replays after the frozen pypdf
  normalization contract.
- `mode=page_section_paraphrase`: only when a figure, equation, or layout cannot yield a faithful text
  anchor; it requires `page`, `section`, a short `supporting_excerpt`, and a reason exact replay is
  impossible. A paraphrase is never represented as an exact quote.

## Blind dual coding and adjudication

Coder A and coder B independently assign all seven fields to the same three frozen method paths using
this version. Coder B receives only this codebook, the sealed blank packet, and the three hash-bound
PDFs; coder B must attest that coder A values and the full repository were not accessed before
submission. Exact agreement is derived from the two assignment maps, never self-reported.

Every disagreement preserves both coder values and locators and goes to a third adjudicator who is
neither coder. The adjudicator selects one allowed value and records a rationale; unresolved source
ambiguity becomes `UNKNOWN`. No disagreement is averaged, majority-voted, or silently discarded.

The current coder-A rows are a v2 recode of AudioToolAgent (`2510.02995`), Thinking While Listening
(`2509.19676`), and Native Active Perception (`2606.19341`). They remain non-load-bearing until a blind
coder-B pass and all adjudications complete.
