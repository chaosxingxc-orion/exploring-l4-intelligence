# Screening contract v2: speech/omni agent root

## Root question

The reproduction program starts from one object only:

> A multimodal agent whose load-bearing input includes speech/audio, operating as an external control
> plane around a frozen black-box omni model.

Artifact availability is evaluated only after a paper passes this root. A paper being easy to reproduce
does not make it a reproduction target.

## Ordered gates

### G0 - load-bearing speech/audio modality

Pass only when waveform, speech, acoustic events, music, or an omni task with indispensable audio
evidence is a load-bearing input to the evaluated system.

- Text-only agents fail G0.
- Image/video-only VLM agents fail G0, even if the paper calls them multimodal or omni.
- Audio generation with no speech/audio reasoning input is modality-adjacent, not a direct pass.
- `TTS` means test-time scaling unless the paper actually performs text-to-speech.

G0 failure routes to `METHOD_ONLY_NON_SPEECH`. Record the transferable method, then stop. Do not spend
time reproducing its dataset, baseline, leaderboard, or historical API score.

### G1 - agentic external control

Pass only when the deployed method performs sequential external control such as observation, tool use,
evidence acquisition, memory update, evaluation, routing, repair, selection, budget allocation, or
stopping.

Speech encoders, MEG decoders, ordinary classifiers, and static aggregation without an action loop route
to `SPEECH_NON_AGENT_BOUNDARY`. They can inform representations or metrics but are not reproduction
targets for W1.

### G2 - frozen black-box compatibility

Pass only when the load-bearing method does not require weight updates, architecture changes, gradients,
hidden states, attention, or guaranteed token log-probabilities from the core model.

Speech/omni agents learned through SFT, RL, adapters, soft prompts, or new model heads route to
`TRAINED_OMNI_BOUNDARY`. Absorb their topology and failure modes; do not reproduce their training path
for the training-free W1 program.

### G3 - reproduction readiness

Only G0+G1+G2 papers receive the three-axis audit:

1. Can the external technique be copied without guessing a load-bearing component?
2. Is the speech/omni evaluation data local or currently obtainable?
3. Can a same-backbone local/API baseline run?

This gate produces `REPRODUCE`, `CLEAN_ROOM`, or `WAIT_FOR_ARTIFACT`. Dataset availability never revives
a paper that failed G0-G2.

## Use of non-speech literature

Text and visual work remains valuable for method absorption. Extract only reusable control objects:

- state and memory representation;
- reward, verifier, critic, or confidence signal;
- search, routing, tool, repair, selection, and stopping actions;
- retry and equal-compute controls;
- verifier false-accept/false-reject and over-iteration failure modes;
- provenance, information-boundary, cost, and rollback rules.

Do not create reproduction tasks, dataset fetches, baseline matrices, or environment builds for these
papers unless a later owner decision widens the root.

## Scope statement

This contract changes reproduction priority, not the Stage-1B evidence record. The earlier 67-paper
resource audit remains valid provenance, but its A/B/C availability labels are not an experiment queue.
This is still mapping and planning; no model, dataset, metric, or prototype execution is authorized.
