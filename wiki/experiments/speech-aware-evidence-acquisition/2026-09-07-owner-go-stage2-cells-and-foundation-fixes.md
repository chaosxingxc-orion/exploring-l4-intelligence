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

## Decision 1 — WSL memory cap (answer `可以` ("yes"))

`.wslconfig` is lowered to `memory=44GB` with `[experimental] autoMemoryReclaim=gradual` (backup
`.wslconfig.bak-20260907`), applied with `wsl --shutdown`. The serving monitor gains host-memory
sampling (study E7c) and `serving_session.sh start` refuses below 12 GB host free.

## Decision 2 — KC-E1 recovery re-registration (answer `继续` ("continue"))

The one permitted recovery of `SAEA-E21-KC-E1-BRIEF-44-V1` is registered with run-cumulative ceilings
(1,520 + 1,750 = 3,270 calls; 285,000 speech seconds; the realized GPU-hours plus 1.6), and the
preregistration's section-6 envelope for both cells is amended accordingly (KU-E1c keeps 1,750 /
150,000 / 1.6). The raise is headroom, not new exposure: all 44 calls were exposed many times over.

## Decision 3 — Audio2Tool 16 kHz re-lock consequence (answer `统一` ("agreed"))

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

## Decision 5 — Earnings-22 knowledge enhancement (answer `如果E22对齐了之后，其实可以对他进行知识加强的` ("once E22 is aligned, it can be knowledge-enhanced too"))

Earnings-22 is not confined to the WER anchor. With the short-form alignment closed (test 9.24
under the silence-tail convention), a knowledge cell on the E22 DEV clips is admitted for
preparation: the knowledge source is the Earnings-22 corpus metadata only (company, ticker,
sector, region, call date — what a participant holds before the call), never a reference
transcript or anything derived from one, with a token-matched placebo as the form twin; the flight
decision follows the KC-E1 verdict. The test split is not read again.

Addendum, same session (answer `E22不需要对外部信息做搜集，不然你最终结果没法和学术参考进行有效对比` ("E22 must not collect external information, or the final result cannot be compared with the academic references")):
no corpus-external source of any kind enters the E22 brief — no public ticker-to-company
table, no filings, no listings. The brief is the corpus metadata file alone (ticker, country, region,
dialect family), so the cell stays comparable with the published Earnings-22 numbers.

## Decision 7 — KC-E1f GO (answer `GO，KC-E1f 准备好后起飞` ("GO, fly KC-E1f as soon as it is ready"))

After the KC-E1 verdict (REJECTED as HARMFUL under its rule: PERSON entity WER +4.15 pp CI90 [+2.63, +5.74],
content-driven, but the corpus-WER and numeric-accuracy guards fail because the whole-prompt brief makes the
core transcribe less, deletions +2,692), the owner admits KC-E1f: the same capped brief consumed as a
second-pass entity repair on the USE axis (pass 1 = the sealed comparator's hypotheses; pass 2 sees audio +
pass-1 text + brief and may emit only span-bounded substitutions; one contact per window; token-matched
twin KU-E1fc). It flies on the Earnings-21 session as soon as its preregistration, prompt fit and wire check
close, ahead of the Audio2Tool and SLURP items of Decision 6.

## Decision 8 — the Earnings-21 silence tail, the promotion recovery, and memory reclaim (2026-09-08, answer `按你的建议走` ("go with your recommendation"))

The Earnings-21 silence-tail cell (`SAEA-E21-FULL44-TAIL2S-V1`: corpus WER 8.200 -> 7.271, -0.93 CI90
[-1.05, -0.79], but PERSON entity WER +0.69 [+0.13, +1.35], NOT ADMITTED under the imported margin) does not
re-lock the Earnings-21 comparator yet. Before any re-lock the study measures Earnings-21's own greedy null
with one comparator replicate at the comparator's geometry (np6, about 1 GPU-hour); the adoption decision
follows that measurement. KC-E1f keeps its preregistered base (the sealed 8.200 comparator). The SLURP `@ts2`
packet promotion takes its one recovery re-registration (+3 speech seconds of ceiling for the last row, after
a crashed gate attempt's real spend) in a no-server gap, and at that gap `.wslconfig` switches
`autoMemoryReclaim` to `dropcache` with a `wsl --shutdown`.

## Decision 9 — five answers of 2026-09-08 (answer `决策项1：A，决策项2：A，决策项3：同意，决策项4：A；决策项5：确认` ("item 1: A, item 2: A, item 3: agreed, item 4: A, item 5: confirmed"))

1. KC-E1f is re-decided (a v2 verdict row, zero contacts) under non-inferiority guards whose margins come from
   the Earnings-21 own-null replicate (margin = the null's CI90 half-width per metric); the v1 REJECTED record
   stays beside it.
2. The Earnings-21 comparator stays the sealed 8.200 direct baseline; the silence tail is recorded as a measured
   OBS convention beside the WER anchor, not adopted, because the paper-facing Earnings metric is the agentic
   entity metric and the tail worsens PERSON.
3. Family rule: every "not worse" guard in a preregistration is a non-inferiority test with a margin fixed in
   advance from the carrier's own noise measurement (Earnings-21: the replicate; SLURP: the measured 28 %
   greedy flip rate; Audio2Tool: the imported greedy null), never a margin-less superiority test.
4. Stage 2 exploration continues (KU-S3, OBS-E1, KU-A1) before any candidate freeze.
5. The SLURP silence-tail cell's row cites Decisions 3 and 6 as its GO.

## Direction — speech-to-knowledge matching (owner thought, 2026-09-08)

The owner adds a research emphasis, quoted in substance: intent matching and its improvement have had too little
attention; in the agentic era the AI understanding audio intent DIRECTLY is where the value lies. Under that
hypothesis the study should systematically explore how speech signals (multi-speaker) are matched to already
constructed knowledge domains, in three dimensions: (1) text-domain knowledge; (2) existing speech-domain
knowledge — the same speaker's semantically diverse expressions of one intent; (3) state knowledge that raises
business performance. These are exactly the richer information sources a multimodal generative model can take
in and a discriminative model (conventional ASR) cannot. The coordinator's analysis and the proposed program
are recorded in the study (readiness note to follow) and summarized in the session transcript.

## Direction — the agent system, its harness and its admission gate (owner instructions, 2026-09-08)

Four instructions given in sequence the same day, quoted in substance:
1. The cells had been transferring the whole task load onto single calls of the frozen core; the study builds an
   agent SYSTEM whose system-level optimization lowers the core's burden and raises task performance
   systematically; consider a ReAct-style revise stage that evaluates quality and proposes revisions.
2. The agent definition must converge to a few named agents calling each other in a loop, with a planning
   mode, and with observation modes chosen per task (a meeting task calls speaker diarization, a noisy input
   calls enhancement, the loop listens selectively to the key audio worth improving).
3. Analyse and abstract the tools -- general and task-specific -- the agents call, supply them uniformly,
   and design and implement on the openJiuwen framework; reuse the existing openJiuwen-based implementation
   unless it is completely unreusable.
4. Standardize the agent harness on `rails` so it is reused across tasks (never one agent system per task);
   before any large-scale test of the engineering base, ensure every module of the division brings a positive
   gain or at least does not hurt the baseline.

Coordinator's response: the design note `docs/readiness/2026-09-08-agent-system-episode-and-core-pressure-v1.md`
(four agents Planner / Observer / Solver / Reviewer in one loop; three mode tables; the tool layer on openJiuwen
local tools; the core-pressure covariates), a read-only assessment of the existing openJiuwen implementation, and
the MODULE ADMISSION GATE: each harness module (a planner rule, an observe mode, a knowledge view, a judge, a tool)
carries a per-carrier admission receipt -- module on vs off, paired, non-inferiority with the carrier's own null
margin, positive gain preferred -- and the harness's default plan contains only admitted or neutral modules.

## Decision 10 — the SLURP intent line (answer `可以，按照你的建议走，先锁定单模型的工程基线，之后再进行详细分析` ("yes, follow your recommendation: lock the single-model engineering baseline first, then the detailed analysis"); 2026-09-08)

After MF-8 (`SAEA-SLURP-MF8-SPEECH-TO-KNOWLEDGE-AUDIT-V1`: 999 of 1,000 DEV rows have their speaker in TRAIN;
gold-free candidate recall on the comparator's errors 86.6 % at k = 8 from scenario-legal top-3 plus the
Nemotron speech vectors; the legality judge flags 42 rows at 100 % precision; multi-audio prompts are supported
on both transport routes; k = 8 exemplars cost 337 tokens): the SLURP session flies, in order, the silence-tail
cell, the SLURP own-null replicate (1,000 contacts, the margin source), KU-S3, KU-S4N (candidate narrowing only:
the core chooses among about eight system-selected candidates), then KU-S4a (same-speaker audio exemplars) with
its twins KU-S4b (other-speaker) and KU-S4c (TRAIN gold text); the primary stratum is the rows whose candidates
are all covered by the speaker's own exemplars (658 of 1,000 at k = 8), all rows secondary; the fallback for an
uncovered slot is "no exemplar", counted as a covariate. The owner also asks for an improvement plan on SLURP
slot filling, where the study's SLU-F1 (44.35 after KC-S1b) sits below the published zero-shot line (WHISMA
63.3) and the trained pipelines (69.5-76.8).

## Decision 11 — five answers of 2026-09-08, evening (answer `决策A：GO，同时要扩展下…决策B：GO…决策C：reviewer不去给修改建议，就是criticism；决策D：提交修改；决策E，按照你的建议走` ("decision A: GO, and widen it as well; decision B: GO; decision C: the reviewer gives no revision suggestions, it is criticism only; decision D: commit the changes; decision E: go with your recommendation"))

A. KU-S3v (static slot-value cards) is GO, and the local-optimization stage of the slot task is WIDENED to the
   whole knowledge-view space: type descriptions, few-shot exemplars, vocabulary cards, and retrieved knowledge
   are all candidates, each admitted one at a time with its form twin under the family rule.
B. The openJiuwen change list items #1-#6 are GO (Reviewer seam and JUDGES registry; registration of the existing
   judges; relaxation of the frozen-packet invariant for registered derivations; the Observer seam; the tool
   catalog with ToolCard manifests and the first eight wrappers with byte-equivalence tests; the four config
   tables with a null arm), planned as parallel worktree waves merged serially; #7-#9 follow the GPU queue.
C. The Reviewer is CRITICISM ONLY: it scores and flags, it never proposes a revision; revisions are the Solver's,
   under the system's constraints.
D. The pending umbrella changes are committed as found (umbrella commit of the same day); the study's P-EMB
   pins are re-pinned against the committed lock.
E. The GPU order follows the coordinator's recommendation: the Earnings-21 series first (OBS-E1, the dispatcher
   admission, the KC-E1f replication), then Audio2Tool, then the SLURP line.

## Decision 12 — four answers of 2026-09-08, late (answer `决策项F：按你建议走，注意并行执行；决策项G：GO；决策项H：这个看下数据集和任务项是否支撑吧，应该还需要调研下本地可部署的最新最强的模型是什么；决策项I：按你建议走` ("item F: go with your recommendation, and mind parallel execution; item G: GO; item H: first check whether the datasets and task items support it, and also survey what the latest and strongest locally deployable model is; item I: go with your recommendation"))

F. openJiuwen items #7-#9 are done as parallel worktree waves merged in GPU gaps: #7 rails standardization
   (register the unregistered ids, fold the two out-of-base controllers, dispose of the launcher directories),
   #8 PORT the Earnings-21 obs path onto the openJiuwen graph (the `window_hook` seam), #9 move Earnings to
   `FlightRuntime` and retire the legacy contact executor.
G. The first whole-loop Earnings-21 cell (plan -> speaker-turn units + brief state -> sealed draft -> judges flag
   -> selective re-listen with context -> substitution-only revise -> commit) is GO for model-free preparation;
   it flies after the SLURP line.
H. Speech enhancement as an observe mode: first check whether the datasets and tasks support it (the Audio2Tool
   noisy tier, the far-field SLURP recordings, the Earnings calls), and survey the latest, strongest locally
   deployable enhancement models; no experiment before that survey.
I. Default plans and the candidate freeze wait for the KV and KU-S4 families; replicated modules enter the
   default plans then.

## Decision 13 — five answers of 2026-09-09 (answer `决策J：你提醒我了，我希望你做一组实验去分析下，是否可以在observe阶段用短语音快速生成草稿，然后在plan阶段接受长语音和前置草稿，让模型去系统性的刷新一次？决策K：按你的建议走；决策L：A；决策M：按你的建议走；决策N：按你建议走` ("decision J: you reminded me; I would like a group of experiments to analyse whether the observe stage can quickly generate drafts from short speech and the plan stage can then take the long speech together with the prior drafts and let the model refresh once, systematically; decision K: go with your recommendation; decision L: A; decision M: go with your recommendation; decision N: go with your recommendation"))

J. Instead of flying OBS-E1b as prepared, the owner asks for an experiment GROUP on a two-pass design: in the
   Observe stage the short speech units (speaker turns) produce drafts quickly; in the Plan stage the model
   receives the LONG speech (the 90-s window) together with the prior drafts and refreshes the transcript
   once, systematically. The coordinator prepares the family (the sealed OBS-E1 unit outputs serve as the
   pass-1 drafts at zero new contacts; pass 2 = long window + stitched draft; a free-refresh arm and a
   substitution-constrained arm; a self-draft twin that feeds the comparator's own long-window hypothesis
   back; comparators = the sealed comparator, OBS-E1 and KC-E1f). OBS-E1b stays prepared, not registered.
K. Family rule adopted: paired arms fly inside the same server process wherever possible; when they cannot,
   the non-inferiority margin comes from a same-day, same-process replicate. Reads of cross-process pairs
   say so.
L. Option A: the legacy contact executor stays unreachable-by-accident; the 32 SLURP speech-native baselines
   are rewritten as phase programs per carrier before Stage 2B, without GPU, not now.
M. The SLURP session runs in the coordinator's order (tail, own null, logprob probe, KV-0, KV-2, KV-1, KV-3,
   KU-S3, KU-S4N, KU-S4a/b/c, KC-S1b replication).
N. The depth-2 dispatcher admission is deferred to the end of the Earnings-21 session.

## Decision 14 — three answers of 2026-09-09 and a statistics ruling (answer `决策O：按你的建议综合对比后形成方案基线；决策P：按你的建议来；决策Q：同意；…两类都大差不差，我们没必要花费过多的GPU时来反复复核这个指标，毕竟这个指标目前也只是在dev集上跑` ("decision O: as you recommend, form the scheme baseline after a consolidated comparison; decision P: as you recommend; decision Q: agreed; ... the two kinds differ little, and we need not spend too many GPU hours re-verifying this metric repeatedly, since for now it only runs on the dev split"))

O. Statistical power on SLURP: fly the preregistered single-pass cells on DEV-1000 first; only a promising arm that
   lands in the grey band (inside the own-null band but positive) earns extra resolution, and then the cheapest
   adequate step (a second pass averaged, or a larger roster after the same-roster replication rule is met);
   the comparison is consolidated into a scheme baseline.
P. Earnings-21 session order: DR-1c -> DR-1f -> DR-1s -> E21-LOOP-1 -> the depth-2 dispatcher admission; OBS-E1b
   stays prepared and unflown.
Q. A study-side Stage-2 results ledger (one row per cell: rule, numbers, status, admission entry, citable sentence)
   is produced, model-free, in parallel.
Statistics ruling: the owner sees two acceptable summaries -- the mean over N repeated runs, or the best of N -- and
does not want GPU hours spent re-verifying a metric that is only measured on the DEV split. Coordinator's reading:
single passes with the carrier's own null margin remain the default; a second pass only for grey-band arms where it is
cheap and decisive; means are the estimate, best-of-N is never used for admission (selection bias) and, if ever
reported, is labelled as an optimistic bound.

## Decision 6 — GPU order (answer `按你的逻辑走` ("follow your logic"))

Earnings-21 session (KC-E1 re-fly, KU-E1c, the silence-tail cell) → Audio2Tool session (`@16k`,
`@16k+ts2`) → SLURP session (silence-tail cell, KU-S3) → OBS-E1 once its seam lands; ready-first
scheduling within that order, the core resident per geometry.

## Provenance

Study repository master at `bfab2b16` (recovery registered); the aborted attempt id
`attempt-20260907T142632Z-a388ef`; the serving session stop record
`SPEECHRL_DATA_DIR/serving/e21-np6-c36864-20260907/session-stop.json`.
