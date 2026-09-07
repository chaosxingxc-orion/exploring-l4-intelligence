# Owner decisions — foundation fixes, Stage-2 GO, E22 knowledge, GPU order (2026-09-07)

Owner decisions recorded from the 2026-09-07 session, in substance. The owner's answers were given
in Chinese; each is quoted once in its original characters and glossed in English, per the program's
first principle. Nothing else in this record is non-English.

## Context

The KC-E1 flight (`SAEA-E21-KC-E1-BRIEF-44-V1`, the ConEC pre-meeting brief on Earnings-21) aborted at
42 of 44 calls on 2026-09-07 when the Claude Code host watchdog killed the always-on serving wrapper
for host memory pressure: `.wslconfig` allowed the WSL VM 56 GB of a 63.4 GB host, and the llama-server
GGUF mmap plus page cache filled it. Nothing of the dead attempt is scored; its spend (1,520 calls,
134,821 speech seconds) is durable. The coordinator put four questions to the owner.

## Decision 1 — WSL memory cap (answer `可以`, "yes")

`.wslconfig` is lowered to `memory=44GB` with `[experimental] autoMemoryReclaim=gradual` (backup
`.wslconfig.bak-20260907`), applied with `wsl --shutdown`. The serving monitor gains host-memory
sampling (study E7c) and `serving_session.sh start` refuses below 12 GB host free.

## Decision 2 — KC-E1 recovery re-registration (answer `继续`, "continue")

The one permitted recovery of `SAEA-E21-KC-E1-BRIEF-44-V1` is registered with run-cumulative ceilings
(1,520 + 1,750 = 3,270 calls; 285,000 speech seconds; the realized GPU-hours plus 1.6), and the
preregistration's section-6 envelope for both cells is amended accordingly (KU-E1c keeps 1,750 /
150,000 / 1.6). The raise is headroom, not new exposure: all 44 calls were exposed many times over.

## Decision 3 — Audio2Tool 16 kHz re-lock consequence (answer `统一`, "agreed")

Pre-approved, conditional on the admission of the `@16k` cell of
`docs/readiness/2026-09-07-a2t-input-rate-standardization-v1-preregistration.md`: the ORG-1 union
4,000 is re-standardized to 16 kHz and re-flown on the standardized media (4,000 contacts, about
23,400 audio seconds, about 1 GPU-hour), with a new D1 supplement and new identity hashes, before any
further Audio2Tool cell. If the cell is not admitted, nothing of this executes.

## Decision 4 — Stage-2 cells GO (answer `GO`)

The two preregistered Stage-2 cells fly under their preregistered rules and budgets, each as one
agent, each with its form twin and equal-contact control:

- KU-S3, `docs/readiness/2026-09-07-slurp-consumption-ku-s3-v1-preregistration.md` (retrieved
  TRAIN slot fillers as typed content on the KC-S1b program; speech-keyed through the pinned
  Omni-Embed-Nemotron vectors);
- OBS-E1, `docs/readiness/2026-09-07-e21-obs-speaker-turn-units-v1-preregistration.md`
  (speaker-turn transport units replacing the fixed 90-second windows; the seam lands first).

## Decision 5 — Earnings-22 knowledge enhancement (answer `如果E22对齐了之后，其实可以对他进行知识加强的`, "once E22 is aligned, it can be knowledge-enhanced too")

Earnings-22 is not confined to the WER anchor. With the short-form alignment closed (test 9.24
under the silence-tail convention), a knowledge cell on the E22 DEV clips is admitted for
preparation: the knowledge source is the Earnings-22 corpus metadata only (company, ticker,
sector, region, call date — what a participant holds before the call), never a reference
transcript or anything derived from one, with a token-matched placebo as the form twin; the flight
decision follows the KC-E1 verdict. The test split is not read again.

## Decision 6 — GPU order (answer `按你的逻辑走`, "follow your logic")

Earnings-21 session (KC-E1 re-fly, KU-E1c, the silence-tail cell) → Audio2Tool session (`@16k`,
`@16k+ts2`) → SLURP session (silence-tail cell, KU-S3) → OBS-E1 once its seam lands; ready-first
scheduling within that order, the core resident per geometry.

## Provenance

Study repository master at `bfab2b16` (recovery registered); the aborted attempt id
`attempt-20260907T142632Z-a388ef`; the serving session stop record
`SPEECHRL_DATA_DIR/serving/e21-np6-c36864-20260907/session-stop.json`.
