---
title: "EXP — the omni's >transcript perception delta is real and task-dependent (in-house directional)"
date: 2026-07-06
stage: 1-directional
purpose: "Boundary-clean in-house test of D0's core research point (omni as a perception ELEMENT): does the frozen omni's direct-audio path carry information beyond its own ASR transcript? Supplements the survey perception-delta lane (which failed external verification)."
---

# EXP — perception delta: omni(audio) vs omni(own-transcript)

> **Boundary-clean** ([[Information-Boundary-Guard]]): both arms are the **same frozen omni**; the transcript
> is the **model's own ASR output** (deployable, reproducible at test — NOT a golden reference). So this is
> exactly the deployment question *"can I replace the omni with (its own) ASR → text-LLM?"* — the flip side
> of the retracted M3. Artifact `_repro/p6_perception_delta.json` (n=60, seed 20260706, prereg-committed).

## Result
| surface | acc audio (A) | acc own-transcript (B) | **delta A−B** | CI | verdict | transcript chars |
|---|---|---|---|---|---|---|
| **SQuAD-zh** (spoken extractive QA, zh) | 0.750 | 0.467 | **+0.283** | [0.133, 0.433] | **SIG(+)** | 46 |
| mmau-mini (audio understanding, en) | 0.700 | 0.583 | +0.117 | [0.0, 0.233] | n.s. (borderline) | 88 |
| vocalbench-zh (short spoken QA, zh) | 0.517 | 0.517 | +0.000 | [−0.1, 0.1] | n.s. | 24 |

## Reading (Stage-1 directional)
1. **The perception delta is real and load-bearing where it matters** — on SQuAD-zh the omni's **direct
   audio** answer beats answering from its **own transcribe→text** by **+0.28 (significant)**. The end-to-end
   audio path preserves information the audio→text→answer path loses. On audio-understanding (mmau) the delta
   is positive but borderline; on very short spoken QA (vocalbench, 24-char answers) the transcript already
   carries the answer, so delta ≈ 0.
2. **This validates D0's core research point**: the frozen omni is a genuine **perception element** — it
   exposes a ">transcript delta" and is **not** losslessly replaceable by (its own) ASR→text-LLM. That is the
   omni's non-commodity value in the [[2026-07-06-omni-agent-elements-vs-usage-framework]].
3. **Honest caveat (the Stage-2 control).** This compares omni-audio vs the omni's **own** (possibly lossy)
   ASR. A **stronger external ASR** (Whisper-large / GPT-4o-transcribe) could narrow the *semantic*-task
   delta (SQuAD) — it cannot narrow the *paralinguistic / audio-event* delta (mmau-style). The survey
   corroborates exactly this: *From Text to Voice* — "when the ASR element is strong, neither architecture
   uniformly dominates; the gap localizes to sensor-element fidelity." So the load-bearing Stage-2 question
   is: **what is the delta over a STRONG external transcriber, and on which task families does it survive?**
   (This is survey GAP-5 / the perception-delta cell.)

## Consequence
- Supports the **omni-as-perception-element** leg of the omni agentic construction plan (D0 frontier item i).
- Feeds D4 candidate **GAP-5** (paralinguistic-conditioned agentic decision with a verifiable-reward
  measure) and the architecture fork (sensor vs brain): the omni's value as a *sensor* is non-trivial only
  where the >transcript delta survives a strong external ASR — a clean Stage-2 pre-registration target.
- Links: [[2026-07-05-t5-headroom-composition]] (perception slice), survey `2026-07-06-perception-delta.md`
  (external lane, contested), `2026-07-06-synthesis.md` GAP-5.
