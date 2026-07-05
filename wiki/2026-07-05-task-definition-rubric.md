---
title: "Task-definition + information-boundary rubric, per semantic family (T1)"
date: 2026-07-05
stage: 1-argumentation
purpose: "Back to the original task definition: for each family, what is the REAL deployment input, what a LEGITIMATE training-free-RL lever may use, and where the boundary is. Gates every experiment (with [[Information-Boundary-Guard]])."
---

# T1 — Per-family task definition + information boundary

> Applies [[Information-Boundary-Guard]] to each semantic family + our on-disk datasets. Two cross-cutting
> rules first, then the per-family table.

## Cross-cutting rules
- **R-input:** the omni's deployment input is **audio** (+ any text the task *legitimately* supplies, e.g.
  a text question that accompanies an audio *content* clip). The **transcript of a spoken input** is NOT
  supplied — hearing it is the task.
- **R-reward (deployable-reward rule):** training-free RL must optimize a reward **computable at
  deployment without the golden label**: self-consistency, confidence, format/rule validity, tool-execution
  success, math re-computation. **WER / accuracy vs the reference are NOT deployable rewards** — they use
  the label; they may only score *oracle ceilings* and *offline dev optimization*, never per-instance
  deployment selection. (This is why oracle-δ is a ceiling, not a lever.)
- **R-fewshot:** demonstrations = (audio, **text task-definition + how-to-handle/reasoning**, answer) from
  **other** items; teach the pattern, never the test item's content.

## Per-family
| Family (datasets) | Deployment INPUT | Target | ✅ Legitimate levers | ❌ Boundary-crossing |
|---|---|---|---|---|
| **ASR / ST** (librispeech; covost2) | audio only | transcript / translation | own-sample best-of-N selected by **LM-likelihood / confidence / consistency**; task-def few-shot (transcription style) | the test audio's **golden transcript** — which *is* the answer; any text of the spoken input = leaking the target |
| **SLU intent+slot** (minds14, slurp, speech-massive) | audio only | intent (+ slots) | own samples; prompt = intent list; few-shot (audio, intent-reasoning, label) from train; **consistency reward**; **memory** of train utterances' intents keyed by the query | the test utterance's golden intent / its transcript |
| **SQA — audio is the CONTENT, question is TEXT** (mmau) | audio + **text question (given)** | answer/choice | own samples; prompt/few-shot; **memory of external facts** for knowledge items; verifiable reward where checkable | the test item's golden answer; a golden transcript of the audio content |
| **SQA — audio IS the spoken QUESTION** (vocalbench, vocalbench-zh, SQuAD-zh, heysquad, spoken-squad, big-bench-audio) | audio only | answer | own samples; few-shot (audio, reasoning, answer) from train; **memory: external knowledge keyed by the query** (the Q1b path); deployable-reward best-of-N | **the spoken question's transcript** (= leaking the input; this is exactly the retracted M3); the golden answer |
| **Speech-Agentic** (voicebench, uro-bench, voiceassistant-eval, tau2) | audio (spoken instruction) | task completion / answer | own rollouts; **tools** (calculator, executor — real resources); **retrieval / memory** (real resources); **task-success / rule reward** (verifiable) | golden answer/transcript of the test item |

## Where each planned lever lands (validity re-grade)
- **T2 few-shot (E7′)** — ✅ if demos are (audio, task-def+reasoning, answer) from train, test audio-only.
- **T3 prompt-opt (E8′)** — ✅ text instruction, no leakage.
- **T4 verifiable-reward best-of-N** — ✅ only where a **deployable** reward exists (math/format/consistency/tool);
  NOT WER/accuracy-vs-golden.
- **T5 headroom composition** — ✅ analyze the model's own samples only.
- **T6 multimodal memory** — ✅ external knowledge, input-keyed, memory built from **train only**, never the
  test item; **especially: never store/inject the test item's transcript** (the M3 line).
- **RETRACTED M3** — ❌ injected the spoken question's golden transcript (row "SQA — audio IS the question").

## Consequence for Q1 (corrected framing)
"Is ICL sufficient?" and "should we build an agentic/memory system?" must both be answered **only with
levers that pass this rubric**. The valid negatives so far (E8/E10/E10b) + the to-be-redone E7′ address
Q1a; the legitimate Q1b candidate is the **multimodal memory** (external knowledge, input-keyed). Any lever
whose gain comes from the ❌ column is inadmissible evidence.
