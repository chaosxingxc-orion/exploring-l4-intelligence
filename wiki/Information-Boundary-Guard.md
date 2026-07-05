---
title: "Information-Boundary Guard — the pre-flight validity check every lever must pass"
date: 2026-07-05
status: STANDING RULE (owner 2026-07-05) — gates every training-free-RL lever/experiment
origin: "M3 retraction — a lever 'worked' by injecting the test item's golden transcript (leakage), invalidating the Q1b lock. Statistical discipline (CIs/controls/review) did NOT catch it; the task-definition + modality-boundary lens did."
---

# Information-Boundary Guard

> **The rule (owner 2026-07-05).** Before ANY training-free-RL lever/experiment runs, it must pass this
> pre-flight check. A lever that improves the metric by using information the real task/deployment does
> not have is **invalid**, no matter how significant the number. This is the safeguard the M3 error
> exposed as missing. Apply it in T1 (per-task) and cite it in every experiment's prereg.

## The four questions (all must be YES)
For a proposed lever L on task T:
1. **Deployment-availability** — does deployment actually HAVE every input L uses? (The omni's task input
   is **audio**. The ground-truth transcript/answer of the *current* item is NOT available.)
2. **Modality-respect** — does L respect the modality the task defines? For an omni model, a lever that
   requires converting the *input* audio to text via an out-of-band ASR **negates the point of the omni
   model** (you'd just use ASR→text-LLM). Processing the query with the omni's OWN understanding is fine;
   substituting a separate clean-text input is not.
3. **No test-item leakage** — does L avoid using the *test item's own* content/answer/transcript? Using
   OTHER items (train demos, a knowledge base, past experience) is fine; using the current item's golden
   in any form is leakage.
4. **Capability, not fed-answer (end-user view)** — from the end user's seat, is the gain a *real
   capability* of the system on the audio input, or is it "we handed the model the answer's input in an
   easier form"?

## Verdicts by example (this program)
| Lever | Passes? | Why |
|---|---|---|
| oracle-over-N (P2), best-of-N over the model's **own samples** | ✅ | uses only the model's own outputs |
| prompt / system-prompt framing (E8), few-shot from **other** items | ✅ | text instruction / demos from train, no test leakage |
| label-free self-selection, two-system verifier (E10/E10b) | ✅ | selects among the model's own samples |
| **verifiable-reward best-of-N** (reward computable at deploy: math re-check, format, consistency) | ✅ | reward ≠ golden label; deployment can compute it |
| **external knowledge-base retrieval / multimodal MEMORY** keyed by the input | ✅ | external knowledge (from a source/train), input-keyed, no test-item answer |
| **M3 — inject the test item's ground-truth transcript** | ❌ **RETRACTED** | deployment has no such input; substitutes a clean-text input for the audio → negates omni; = input leakage |
| acoustic "oracle" over feature-altering transforms (earlier) | ❌ retracted | content leakage at the feature level |

## The subtle line (transcript vs knowledge)
- ❌ **The current item's transcript** = leaking the INPUT the model should perceive.
- ✅ **External knowledge relevant to the query** (a fact from a KB, a handling-pattern from a past
  experience) = a legitimate deployment resource. The multimodal memory system lives on the ✅ side because
  its VALUES are external knowledge stored from training/sources, retrieved by the input's key, and it
  **never stores the test item**.
- ✅ **The omni's OWN transcription/summary of the QUERY** (to build a compressed key) = processing the
  input the system legitimately has — fine, as long as it isn't the ground-truth and isn't the answer.

## Few-shot, done right (the E7 correction)
Few-shot ICL must teach the **task-handling pattern**, not hand over answers: demonstrations = (audio,
**text task-definition + reasoning/how-to-handle**, answer) from **other** items, so the model applies
prior experience to the current audio-only query. Not (audio, answer) pairs; never the test item's content.
