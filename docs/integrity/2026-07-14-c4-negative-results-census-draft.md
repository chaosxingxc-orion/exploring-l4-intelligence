# C4 — Negative-Results Census (ledger) — DRAFT

DRAFT — single-pass AI census (C1/C4), coordinator verification pending; generated 2026-07-14

Scope: umbrella `wiki/` + `docs/`, W1 `git log` + `_repro/`, E:-drive run tree (listing only).
Method: `grep` over `wiki/Decision-Log.md`, `Research-Objective.md`, `Per-Work-Status.md`,
`wiki/survey/*`, `wiki/archive/*`, `docs/claim_ledger.yaml`, `docs/integrity/*`, and both repos' commit
logs. No runs executed. Unknowns marked UNKNOWN; items with no durable home marked **UNRECORDED**.

**Denominator legend** (is the negative visible in the *hot* current-state layer, i.e. would a reader
loading only `Research-Objective.md` see it?):
- **HOT** — surfaced in `wiki/Research-Objective.md` (the daily-load entry point).
- **LEDGER** — in `docs/claim_ledger.yaml` (authoritative, cold but always-consulted for claims).
- **COLD** — only in `Decision-Log.md` / dated wiki artifacts / `wiki/archive/` / commit messages.
- **UNRECORDED** — no durable file; session-log / human-recall only.

---

## Headline

The project keeps an **unusually disciplined negative-results trail**: `claim_ledger.yaml` holds 16
claims of which **6 invalid + 2 null + 1 unverified** carry explicit `invalid_reason`/retraction, and
the hot layer (`Research-Objective.md`) surfaces the current-stage kills (I1, C-T7, IAD collapse-risk,
knowledge-stack PARK, 2 unverified cites). **The main gaps are (a) the GLAP full-corpus build PARK, whose
specific `31000/57638` figure lives only in a commit message + CLAUDE.md, not in any hot-layer status;
and (b) the config-selection-trajectory negatives ("which abandoned sweeps didn't help"), which the
integrity apparatus itself declares UNRECORDED (session-log/human-recall only).**

Row count: **29**. UNRECORDED (no durable home): **2** (rows 27, 29); PARTIAL/at-risk of falling out of
the denominator: **4** (rows 19, 20, 26, 28).

---

## Ledger

| # | Negative / failed / aborted item | What happened | Where recorded (file / commit) | Grade | Denominator |
|---|---|---|---|---|---|
| 1 | **C-T7 heysquad RAG leakage** | H0=+0.517 CI[.38,.65] RETRACTED as answer-lookup (info-boundary violation); clean rerun H0=**−0.066** null | `claim_ledger.yaml` C-T7 (status invalid); `Research-Objective.md` L81; Decision-Log 续33勘误; `wiki/2026-07-07-E6-final-conclusions-clean` | invalid (adjudicated) | HOT+LEDGER |
| 2 | **C-M3 cross-modal support-expansion** | +22.4% RETRACTED — injected "new signal" was the test-item gold (leakage) | `claim_ledger.yaml` C-M3 (invalid); umbrella commit `a5f92ba`; `wiki/2026-07-05-A-realization-conclusion` retraction banner | invalid | LEDGER+COLD |
| 3 | **M3 Phase-0 KILL** | pooled entity-match F=**0.38108** vs frozen 0.01 kill threshold → mechanical KILL (30B already emits "rare" entities) | W1 commit `1b53b46`; `_repro/m3_phase0_zero_support.json`; Decision-Log ~L1132 | kill | COLD |
| 4 | **C-ASR-SEEDS seed-stability** | "3 generation seeds" INVALID — cohort/noise/decode-path/pool all varied together, not isolated RNG replicates | `claim_ledger.yaml` C-ASR-SEEDS (invalid) | invalid | LEDGER |
| 5 | **C-MINDS-POLICY** | INVALID as zero-shot RL-selection — transductive fixed 3-shot policy, not mechanism | `claim_ledger.yaml` C-MINDS-POLICY (invalid); superseded_by C-MINDS-V2 | invalid | LEDGER |
| 6 | **C-W4-DISENTANGLE** | acceptance criterion unmet — diagonal_dominant=False; downgraded L2/L3→L0/L1 | `claim_ledger.yaml` C-W4-DISENTANGLE (invalid); `wiki/2026-07-11-adversarial-review…` §3.3 | invalid | LEDGER+COLD |
| 7 | **C-PHASEA "executable"** | INVALID — scheduler PLAN-ONLY (NotImplementedError all 6 arms); "prep complete" = bookkeeping-false. Later fixed (续15) | `claim_ledger.yaml` C-PHASEA (invalid, +successor note); W1 `52aa61a`→`28f0a38` | invalid (then remediated) | LEDGER+COLD |
| 8 | **Phase-A DEV sweep HALTED** | SWEEP HALTED before any of 140 cells ran — wrong object (squtr/vocalbench KB "value" was the query's OWN text, not the retrieved doc) | `claim_ledger.yaml` C-PHASEA note; Decision-Log 续15 | aborted (0/140) | LEDGER+COLD |
| 9 | **C-ASR-MBR** | MBR selection NULL (n.s. under corpus metric) | `claim_ledger.yaml` C-ASR-MBR (status "null") | null | LEDGER |
| 10 | **C-W4-EMO emotion pooling** | flagship +0.097 was single-seed; across-seed 95% t-CI **[−0.043,+0.116]** spans 0 → NULL | `claim_ledger.yaml` C-W4-EMO ("null"); Decision-Log 2026-07-02 ~L1240; `wiki/archive/2026-06-24-emotion-pooling…` | null | LEDGER+COLD |
| 11 | **C-W4-PARA speaker/paralinguistic** | UNVERIFIED (does not meet its bar as stated) | `claim_ledger.yaml` C-W4-PARA (unverified) | unverified | LEDGER |
| 12 | **A-realization Phase-2 DIRECTIONAL NULL** | under frozen +10% bar, no in-fence lever realizes the gain; over-reach corrected 3× | umbrella `fbd1115`, `d52a8e7`; `wiki/archive/2026-07-05-A-realization-conclusion`; Decision-Log ~L973 | directional null | COLD |
| 13 | **Q1 ICL-insufficiency** | 4 read-out levers all fail → new-info needed (owner-gated) | umbrella `a46b089`; `wiki/archive/2026-07-05-Q1-conclusion-corrected` | directional | COLD |
| 14 | **T2 task-definition few-shot** | PROPER task-def few-shot ALSO fails to beat plain (closes E7 mis-design gap) | W1 `dbaed43`; `_repro/t2_taskdef_fewshot.json` / `e7_fewshot.json` | null | COLD+LEDGER(via C-BASELINES artifacts) |
| 15 | **T3 iterative prompt-opt** | NO gain on any surface (last read-out lever) | W1 `3a4804c`; `_repro/t3_iterative_promptopt.json` | null | COLD |
| 16 | **E6 acoustic-oracle-over-K** | REVERTED — semantic content leakage / invalid (owner) | W1 `7f25898` | invalid/retracted | COLD |
| 17 | **W5 collapse / omni-embed "selection"** | deep review collapsed W5 (VoI≈0); the omni-embed "selection" never used the reward (argmax cosine, not reward) — same accounting-identity flaw | Decision-Log 2026-07-02 ~L1185–1200 | null/collapse | COLD |
| 18 | **length selector HARMFUL (noise2)** | length-based selector significantly HARMFUL in noise2 realization | W1 `fc9e17c`; `_repro/asr_bon_v2_snr5_noise2.json` | negative (harmful) | COLD |
| 19 | **GLAP full-corpus embedding build PARKED** | build halted at **31000/57638** (~54%); only `full_corpus__fiqa__glap.npz` on E:; parked per 续28 | W1 `64d697c` commit msg; CLAUDE.md env note; Decision-Log 续28 ("数据尾巴…GLAP 全语料嵌入待 CPU 空窗"); E: `_repro/full_corpus_checkpoints/` | parked (incomplete) | **PARTIAL** — the `31000/57638` figure is only in the commit msg + CLAUDE.md; not in `Research-Objective.md`/`Per-Work-Status.md` |
| 20 | **GLAP CUDA blocked** | vendored `modeling_glap` bug blocks CUDA → CPU default stays | W1 `64d697c` | known blocker | **PARTIAL** (commit-only) |
| 21 | **I1 general label-free selector KILLED** | DIRECT_OCCUPIED — MBR on frozen speech beats beam at equal-K on our datasets; MBR correction made the kill STRONGER | `Research-Objective.md` L27/L50; `wiki/2026-07-14-stage1c-decision-package.md`; `survey/2026-07-14-coverage-and-kill-matrix-v2.md`; Decision-Log 续36/续38 | SCOUT kill (hypothesis-grade) | HOT |
| 22 | **IAD collapse risk (pre-registered)** | IAD 2504.01931: agentic loop beat one-shot best-of-N by only **~3–4 pts**, front-loaded → pre-registered collapse risk for the agentic-loop object | `wiki/2026-07-14-stage1c-decision-package.md` L75–76; `2026-07-14-p0r-response…` L107; `Research-Objective.md` L33 (IAD=预登记坍缩风险) | pre-registered risk (survey) | HOT |
| 23 | **2 UNVERIFIED citations** | 2512.10170 / 2512.10403 — network NOT_RESOLVED, could not verify | `wiki/2026-07-14-stage1c-decision-package.md` frontmatter L11; `Research-Objective.md`; survey round-2 targets | unverified | HOT |
| 24 | **WebFetch blockage (this week)** | WebFetch blocked + 2 cites NOT_RESOLVED — cited against the "deterministic compile" claim | `wiki/2026-07-14-response-to-knowledge-stack-evaluation.md` L83 | tooling blockage | COLD |
| 25 | **Knowledge-stack selection PARKED** | llm-wiki-compiler pilot proposal → owner SHELVE-ALL after six-lens adversarial review (revive via 4 gates post-Stage-1C) | `Research-Objective.md` L64–67 (续37); Decision-Log 续37; `wiki/2026-07-14-response-to-knowledge-stack-evaluation.md` | owner-shelved | HOT |
| 26 | **8 broken-variant baseline cells** | UnderEmotion-en/zh + vocalbench-emotion on qwen3-omni-30b; `.broken-/broken2-20260710.json` | `experiment_attempt_registry.jsonl` (status=broken-variant, 8 rows) | broken/superseded | **PARTIAL** (registry-only; no narrative adjudication) |
| 27 | **Config-selection-trajectory negatives** | every tried-and-abandoned prompt/weight/threshold/K/embedder sweep + WHY it was dropped — the "what didn't work" corpus | Declared unrecoverable-from-disk in `prior_exposure_registry.json` `manual_completion_todo[0]`; `p0_gate_status`=NOT_PASS | negative (multiplicity) | **UNRECORDED** (session-log/human-recall only) |
| 28 | **Survey literature negatives (D4)** | 53 negative findings across 33 problems / 101 verified claims (lit-side kills, e.g. no traditional hotword family survives chat-API omni) | umbrella `b46df8b`; `survey/2026-07-04-*`, `2026-07-12-omni-hotword-biasing-survey.md` | lit negatives (survey-grade) | COLD (survey docs) |
| 29 | **vLLM / int4 path OOM (Qwen3-Omni)** | HF/vLLM int4 path OOMs → switched to llama.cpp GGUF (the path that produced the real best-of-N) | E: `_repro/step0_evidence/vllm_attempt.log`, `_repro/vllm_probe.log`; mem0 note "qwen3-omni-30b-llamacpp" | known blocker | **UNRECORDED** in wiki/ledger (raw log + personal-memory only) |

---

## Notes on grading and denominator

- **Hot-layer coverage is selective (by policy, not by omission).** The hot/cold record policy
  (`docs/integrity/record-policy-and-attestations.md`) intentionally keeps `Research-Objective.md`
  bounded, so the experiment-level W1 nulls/kills (rows 3, 12–18) correctly live in the cold layer +
  `claim_ledger.yaml`. That is compliant. The concern is only where a *live/open* liability sits in an
  easily-missed place — see rows 19/20 (GLAP PARK), 26 (broken cells), 29 (OOM).

- **Two genuine UNRECORDED items:**
  - **Row 27 (config-selection trajectory)** is the load-bearing one — it is simultaneously the C1 gap
    and a C4 negative-results gap: the population of "sweeps that didn't help" is not durably written
    anywhere, which is exactly what a multiplicity/QRP reviewer needs. The project flags it honestly
    (`p0_gate_status`), so it is *acknowledged-but-uncaptured*, not hidden.
  - **Row 29 (vLLM OOM)** exists only as a raw E: log + personal mem0 note; no wiki/ledger entry.
    Low stakes, but by the C4 rule it is UNRECORDED in durable team memory.

- **Partial/at-risk of dropping out of the denominator:**
  - **Rows 19–20 (GLAP):** the `31000/57638` progress figure and the CUDA-block cause survive only in
    commit `64d697c`'s subject + CLAUDE.md; a reader of `Research-Objective.md` / `Per-Work-Status.md`
    would not see that the full-corpus index is ~54% built and parked. Recommend a one-line
    Per-Work-Status entry.
  - **Row 26 (broken cells):** captured only as registry rows with `status=broken-variant`; no prose
    saying *why* they broke or whether the replacements are clean.
  - **Row 28:** survey negatives are recorded but scattered across many dated survey files; fine for
    cold archive, hard to enumerate.

- **Consistency check:** every `invalid`/`null`/`unverified` claim in `claim_ledger.yaml` (16 total:
  6 invalid, 2 null, 1 unverified, 7 directional) is represented above (rows 1,2,4,5,6,7,9,10,11 +
  directional context). No ledger negative was found that lacks a durable home. No positive claim was
  found resting on a retracted number in the *current* hot layer (the +0.517 and +22.4% figures carry
  explicit "prohibited from citation" banners).

---

## Provenance of this draft
- Evidence snapshot: umbrella HEAD `93e0bcf` (working tree read 2026-07-14); W1 HEAD `a532da0`.
- Method limits: single-pass; `grep`-driven; no runs; binaries not opened; line numbers are from the
  working-tree read and may shift; WSL-side memory/logs not inspected. Coordinator should spot-verify
  rows 19, 26, 27, 29 and the WSL MLflow question from C1 §1.

---

## Coordinator spot-check addendum（2026-07-14，主会话亲验）

- 本文件提交入 git 后即构成 row 27（config-selection 负结果轨迹）与 row 29（vLLM/int4 OOM）的
  **耐久归档**——UNRECORDED → RECORDED_HERE。
- GLAP full-corpus PARK（31000/57638，CUDA 阻塞）已提入热层（Research-Objective open item 6），
  不再只活在 commit 信息里。
- **闭环形态：C4 = CENSUS_COMPLETE**（29 行台账；2 项转正；4 项 PARTIAL 在台账内继续跟踪）；
  **owner 于 1B-0 探针协议签批时终验**。
