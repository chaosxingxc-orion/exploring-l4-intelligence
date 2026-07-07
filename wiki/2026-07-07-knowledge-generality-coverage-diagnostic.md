---
title: Knowledge Organization — Generality & Coverage Diagnostic (WS-C)
date: 2026-07-07
stage: 1-argumentation
lane: knowledge-backbone
inputs: kb_registry.py (code-backed), 2026-07-07-multimodal-knowledge-systems-alignment.md (survey), T0/T7-T10 runs
---

# Knowledge Generality & Coverage Diagnostic

Precise boundary of the "generality gap" flagged 2026-07-07, triangulated across **three independent
coverage lenses**. Scope = speech/omni (audio+text); **no image is a deliberate project boundary, not
a gap** — so generality is tested WITHIN speech, along the key/value axis.

## The reframed generality question

The pre-2026-07-07 knowledge base was, in effect, **"spoken-question (lexical) → text-passage KB"** — a
single narrow band. Generality within speech is NOT "does it cover images"; it is: **does knowledge
organization handle AUDIO-NATIVE / acoustic-grounded knowledge** (key = non-lexical audio: speaker,
emotion, sound-event, scene) **as well as lexical spoken-QA?** The new KB (WS-B) makes audio the KEY by
construction (`kb_registry`: key_modality=audio for all 26 speech datasets), so the organization is now
general in principle; the diagnostic below shows where it is *populated/tested* vs *empty*.

## Coverage matrix — three lenses over 28 datasets

Columns: **KB-cell** = `kb_registry` (key_modality/value_type/status; the organization lens) ·
**Recent-exp** = touched by any T0/T7–T10 knowledge run (the empirical lens; 4/28) ·
**Baseline** = has an admissible (A/B) post-2025.01 baseline (the literature lens; WS-D survey).

| dataset | family | KB-cell (key→value / status) | Recent-exp | Adm. baseline |
|---|---|---|---|---|
| librispeech | ASR | audio→transcript / buildable | — | **A** BR-ASR |
| covost2 | ST | audio→translation / buildable | — | — |
| fleurs-r | ST/LID | audio→translation / buildable | — | — |
| seed-tts-eval | TTS | audio→transcript / buildable | — | — |
| **crema-d** | **SER+SID** | **audio→labels / buildable** | — | **— (EMPTY)** |
| **meld** | **SER** | **audio→labels / buildable** | — | **— (EMPTY)** |
| minds14 | SLU | audio→intent / buildable | — | — |
| slurp | SLU | audio→intent / buildable | — | — |
| speech-massive | SLU | audio→intent / buildable | — | — |
| mmau-mini | audio-understanding | audio→answer / buildable | P6 (perception-delta only) | — |
| mmar | audio-reasoning | audio→answer / buildable | — | — |
| air-bench | audio-benchmark | audio→answer / buildable | — | — |
| mmsu | spoken-reasoning | audio→answer / buildable | — | A (weak, VoxMind sub) |
| big-bench-audio | spoken-reasoning QA | audio→answer / **built** | **T9** | — |
| heysquad | extractive spoken-QA | audio→answer / **built** | **T7/T8** | — (sibling covered) |
| spoken-squad | spoken-QA | audio→answer / buildable | — | **A** WavRAG, Attn-Grounding |
| uro-bench (SQuAD-zh) | ZH spoken-dialogue | audio→answer / **built** | **T9/T10/P6** | — |
| vocalbench | conversational EN | audio→response / buildable | — | — |
| vocalbench-zh | ZH spoken-interaction | audio→answer / **built** | **T9/P6** | — |
| voicebench | spoken-QA+agentic | audio→response / buildable | — | **A** VoxMind |
| voiceassistant-eval | assistant | audio→response / buildable | — | — |
| audiomc | multi-turn | audio→response / deferred | — | **A** Audio-MultiChallenge |
| soulx-duplug | full-duplex | audio→none / n-a | — | — |
| eva-bench | voice-agent | audio→response / deferred | — | **A** EVA-Bench |
| tau2-bench | voice tool-use | audio→response / deferred | — | **A** τ-Voice |
| aime24/25/26 | text-math | text→answer / n-a | — | — |

## The verdict: one narrow band covered, the acoustic-grounded trunk empty across all three lenses

- **Empirical lens (Recent-exp): 4/28 touched** by any knowledge run (heysquad, big-bench-audio,
  vocalbench-zh, uro-bench/SQuAD-zh) — all **audio→answer text-QA**. Every non-QA family (ASR/ST/SER/SID/
  SLU/audio-reasoning) is **empirically untouched** by knowledge work.
- **Organization lens (KB-cell): now general but mostly unpopulated.** `kb_registry` classifies all 28;
  audio-native cells (crema-d/meld SER+SID; mmar/air-bench audio-reasoning) are **buildable** (WS-B made
  them first-class) but **not yet populated** — only 5 sources have ever been built, all audio→answer.
- **Literature lens (Baseline): 7/26 have an admissible baseline; 19 empty.** Crucially, **crema-d/meld
  (SER+SID) have ZERO baseline** — the single most strategic empty cell, and it is exactly the W4
  flagship disentanglement target.

**Triangulated conclusion:** the acoustic-grounded knowledge trunk (key = non-lexical audio → speaker/
emotion/sound labels) is empty in **all three lenses at once** — unbuilt as a populated source, untested
in any experiment, and unbaselined in the 2025-26 literature. The generality gap is therefore real and
precisely located: **we only ever did lexical spoken-QA; acoustic-grounded knowledge is the whitespace.**

## What WS-B changed and what remains

- **Changed (organization):** audio is now the KEY for all 26 speech datasets; audio-native is a
  first-class buildable cell (`kb_build.build_source(key_modality="audio", ...)`), PoC-verified.
- **Remains (population + test, Stage-2):** populate the audio-native cells (crema-d/meld via a real
  acoustic embedder — omni-embed-nemotron-3b / CLAP), and run powered experiments. These are Stage-2;
  Stage-1 delivers the organization + the located gap, not the large-sample result.
- **Cross-ref:** the empty SER/SID cell = the W4 flagship's object → this diagnostic is the concrete
  hand-off from W1's knowledge track to W4's embedding-disentanglement track.
